from alexamd_upload import app, model
from flask import render_template, request, session
from s3utils import s3upload, s3delete
import uuid
import png
import numpy as np
import pydicom

def get_context():
    context = {}
    if 'patient_id' in session:
        context['patient_id'] = session['patient_id']

    return context

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['patient_id'] = request.form['patient']

    context = get_context()
    context['patients'] = []

    db = model.get_db()

    for patient in db.execute('select pid, p_first, p_last from patients'):
        context['patients'].append({'id': patient['PID'], 'name': '{} {}'.format(patient['P_First'], patient['P_Last'])})

    return render_template('index.html', **context)


@app.route('/patient/<int:patient_id>/upload/', methods=['GET', 'POST'])
def upload(patient_id):
    db = model.get_db()

    if request.method == 'POST':
        collection_id = int(request.form['collection'])

        # collection_id < 0 means a new collection should be created
        if collection_id < 0:
            print('Creating new collection with name {}'.format(request.form['new_collection']))
            db.execute('insert into collections(c_name, study, pid) values (?, ?, ?)',
            (request.form['new_collection'], 'Other', session['patient_id']))
            collection_id = db.execute('select max(cid) as new_cid from collections').fetchone()['new_cid']


        print('Adding image(s) to collection with id  {}'.format(collection_id))

        study = db.execute('select study from collections where cid = ?',
                           (collection_id,)).fetchone()['Study']
        cur_idx = db.execute('select max(ind) as start_idx from images where cid = ?',
                               (collection_id,)).fetchone()['start_idx']
        if not cur_idx:
            cur_idx = 0

        for file in request.files.getlist('files'):
            image_id = str(uuid.uuid1())
            db.execute('insert into images(iid, cid, ind) values (?,?,?)',
                       (image_id, collection_id, cur_idx))

            # convert dicom to jpeg. (based off of:
            # https://github.com/pydicom/pydicom/issues/352#issuecomment-406767850)
            try:
                ds = pydicom.dcmread(file)
            except pydicom.errors.InvalidDicomError:
                print('Error: invalid dicom')
                # TODO: alert user of error
                continue

            if study == 'Other':
                study = ds.Modality
            elif study != ds.Modality:
                # TODO: alert user or error
                print('Error: images in collection are of different modalities')

            # Convert to float to avoid overflow or underflow losses.
            image_2d = ds.pixel_array.astype(float)

            # Rescaling grey scale between 0-255
            image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0

            # Convert to uint
            image_2d_scaled = np.uint8(image_2d_scaled)
            image = png.from_array(image_2d_scaled, 'L')

            # upload image object
            s3upload(image_id, image)
            cur_idx += 1

        if study != 'Other':
            db.execute('update collections set study = ? where cid = ?',
                (study, collection_id,))

    context = get_context()
    context['collections'] = []

    for collection in db.execute('select cid, c_name, study from collections where pid = ?',
                                 (session['patient_id'],)):
        context['collections'].append({'id': collection['CID'], 'name': collection['C_Name']})


    return render_template('upload.html', **context)

@app.route('/patient/<int:patient_id>/manage/', methods=['GET', 'POST'])
def manage_patient(patient_id):
    db = model.get_db()

    if request.method == 'POST':
        if 'id' in request.form:
            print('Deleting collection with id {}'.format(request.form['id']))
            for image in db.execute('select i.iid from images i where cid = ?',
                (request.form['id'],)):
                s3delete(image['iid'])

            # TODO: add on delete cascade so all of the collection's images will be deleted
            db.execute('delete from collections where cid = ?', (request.form['id'],))
        else:
            print('Creating new collection with name {}'.format(request.form['name']))
            db.execute('insert into collections(c_name, study, pid) values (?, ?, ?)',
                       (request.form['name'], 'Other', session['patient_id']))

    context = get_context()

    context['items'] = []
    for collection in db.execute('select cid, c_name, study from collections where pid = ?',
                                 (session['patient_id'],)):
        context['items'].append({'id': collection['CID'], 'name': collection['C_Name']})

    return render_template('manage.html', **context)

@app.route('/manage/', methods=['GET', 'POST'])
def manage():
    db = model.get_db()

    if request.method == 'POST':
        if 'id' in request.form:
            print('Deleting patient with id {}'.format(request.form['id']))
            # TODO: test this query
            for image in db.execute('select i.iid from images i join collections c on c.cid = i.cid where c.pid = ?',
                (request.form['id'],)):
                s3delete(image['IID'])

            # TODO: add on delete cascade so all of the patient's collections and images will be deleted
            db.execute('delete from patients where pid = ?', (request.form['id'],))
        else:
            print('Adding patient with name {}'.format(request.form['name']))
            name = request.form['name'].split()
            db.execute('insert into patients(p_first, p_last) values (?, ?)',
                       (name[0], name[1],))

    context = get_context()
    context['items'] = []

    for patient in db.execute('select pid, p_first, p_last from patients'):
        context['items'].append({'id': patient['PID'], 'name': '{} {}'.format(patient['P_First'], patient['P_Last'])})

    return render_template('manage.html', **context)
