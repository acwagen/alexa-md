from alexamd_upload import app, model
from flask import render_template, request, session, flash
from s3utils import s3upload, s3delete
import uuid
import png
import numpy as np
import numpngw
import pydicom
import io
def get_context(patient_id=None):
    context = { 'theme': session['theme'] if 'theme' in session else 'dark' }

    if patient_id:
        db = model.get_db()
        patient = db.execute('select p_first, p_last from patients where pid = ?',
            (patient_id,)).fetchone()
        context['patient_name'] = '{}, {}'.format(patient['P_Last'], patient['P_First'])

    return context

@app.route('/', methods=['GET', 'POST'])
def index():
    db = model.get_db()

    context = get_context()
    context['patients'] = []

    for patient in db.execute('select pid, p_first, p_last from patients'):
        context['patients'].append({'id': patient['PID'],
            'name': '{}, {}'.format(patient['P_Last'], patient['P_First'])})

    return render_template('index.html', **context)


@app.route('/patient/<int:patient_id>/upload/', methods=['GET', 'POST'])
def upload(patient_id):
    db = model.get_db()

    if request.method == 'POST':
        collection_id = int(request.form['collection'])

        # collection_id < 0 means a new collection should be created
        if collection_id < 0:
            app.logger.info('Creating new collection with name {}'.format(
                request.form['new_collection']))

            if request.form['new_collection']:
                db.execute('insert into collections(c_name, study, pid) values (?, ?, ?)',
                    (request.form['new_collection'], 'Other', patient_id))

                collection_id = db.execute('select max(cid) as new_cid from collections'
                    ).fetchone()['new_cid']
            else:
                collection_id = None
                flash('Error: sequence name must not be blank', 'error')

        if collection_id:
            app.logger.info('Adding image(s) to collection with id  {}'.format(collection_id))

            study = db.execute('select study from collections where cid = ?',
                               (collection_id,)).fetchone()['Study']
            cur_idx = db.execute('select max(ind) as start_idx from images where cid = ?',
                                   (collection_id,)).fetchone()['start_idx']
            if not cur_idx:
                cur_idx = 0
            else:
                cur_idx += 1

            # TODO: add progress bar to show how many images are processed
            for file in request.files.getlist('files'):
                image_id = '{}.png'.format(uuid.uuid1())

                print('[DEBUGGING] image_id is {}, file is {}'.format(image_id, file))

                # convert dicom to png. (based off of:
                # https://github.com/pydicom/pydicom/issues/352#issuecomment-406767850)
                try:
                    ds = pydicom.dcmread(file)
                except pydicom.errors.InvalidDicomError:
                    flash('Error: Invalid dicom: {}'.format(file.filename), 'error')
                    continue

                if study == 'Other':
                    study = ds.Modality
                elif study != ds.Modality:
                    flash('Error: Image {} has a different modality than selected sequence'.format(file.filename), 'error')
                    continue

                try:
                    # Convert to float to avoid overflow or underflow losses.
                    image_2d = ds.pixel_array.astype(float)

                    # Rescaling grey scale between 0-255
                    image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0

                    # Convert to uint
                    image_2d_scaled = np.uint8(image_2d_scaled)

                    image = png.from_array(image_2d_scaled, 'L')

                    # save image in memory and upload to s3
                    with io.BytesIO() as image_data:
                        image.save(image_data)
                        image_data.seek(0)

                        # upload image object
                        s3upload(image_id, image_data)

                    # insert into database once everything else has succeeded
                    db.execute('insert into images(iid, cid, ind) values (?,?,?)',
                               (image_id, collection_id, cur_idx))
                    cur_idx += 1

                except NotImplementedError:
                    flash('Error converting image {}'.format(file.filename), 'error')
                except RuntimeError:
                    flash('Error converting image {}'.format(file.filename), 'error')

            if study != 'Other':
                db.execute('update collections set study = ? where cid = ?',
                    (study, collection_id,))

    context = get_context(patient_id=patient_id)
    context['collections'] = []

    for collection in db.execute('select cid, c_name, study from collections where pid = ?',
                                 (patient_id,)):
        context['collections'].append({'id': collection['CID'], 'name': collection['C_Name']})


    return render_template('upload.html', **context)

@app.route('/patient/<int:patient_id>/manage/', methods=['GET', 'POST'])
def manage_patient(patient_id):
    db = model.get_db()

    if request.method == 'POST':
        if 'id' in request.form:
            app.logger.info('Deleting collection with id {}'.format(request.form['id']))
            image_ids = []
            for image in db.execute('select i.iid from images i where cid = ?',
                (request.form['id'],)):
                image_ids.append(image['IID'])
            if len(image_ids):
                s3delete(image_ids)

            db.execute('delete from collections where cid = ?', (request.form['id'],))

    context = get_context(patient_id)

    context['items'] = []
    for collection in db.execute('select c.cid, c.c_name, c.study \
         from collections c where c.pid = ?',
                                 (patient_id,)):
        # this might be able to be combined into the above query
        count = db.execute('select count(*) as count from images where cid = ?',
            (collection['CID'],)).fetchone()['count']
        context['items'].append({'id': collection['CID'],
            'name': '{} ({} {})'.format(collection['C_Name'], count, 'images' if count != 1 else 'image') })

    return render_template('manage_patient.html', **context)

@app.route('/manage/', methods=['GET', 'POST'])
def manage():
    db = model.get_db()

    if request.method == 'POST':
        if 'id' in request.form:
            app.logger.info('Deleting patient with id {}'.format(request.form['id']))
            image_ids = []
            for image in db.execute('select i.iid from images i \
                join collections c on c.cid = i.cid where c.pid = ?',
                (request.form['id'],)):
                image_ids.append(image['IID'])
            if len(image_ids):
                s3delete(image_ids)

            db.execute('delete from patients where pid = ?', (request.form['id'],))

        else:
            app.logger.info('Adding patient with name {} {}'.format(request.form['f_name'], request.form['l_name']))

            if request.form['f_name'] and request.form['l_name']:
                first_name = request.form['f_name']
                last_name = request.form['l_name']

                db.execute('insert into patients(p_first, p_last) values (?, ?)',
                           (first_name, last_name,))
            else:
                flash('Error: patient name cannot be blank', 'error')


    context = get_context()
    context['items'] = []

    for patient in db.execute('select pid, p_first, p_last from patients'):
        context['items'].append({'id': patient['PID'],
            'name': '{}, {}'.format(patient['P_Last'], patient['P_First'])})

    return render_template('manage.html', **context)

@app.route('/settings/', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        session['theme'] = request.form['theme']

    return render_template('settings.html', **get_context())
