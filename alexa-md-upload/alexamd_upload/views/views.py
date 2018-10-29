from alexamd_upload import app
from flask import render_template, request, session
from s3utils import s3upload
import uuid


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['patient_id'] = request.form['patient']

    context = {}
    if 'patient_id' in session:
        context['patient_id'] = session['patient_id']

    # TODO: populate from database
    context['patients'] = [{'id': '1', 'name': 'Patient A'}, {'id': '2', 'name': 'Patient B'}]

    return render_template('index.html', **context)

@app.route('/patient/<int:patient_id>/upload/', methods=['GET', 'POST'])
def upload(patient_id):
    if request.method == 'POST':
        collection_id = int(request.form['collection'])

        # collection_id < 0 means a new collection should be created
        if collection_id < 0:
            print('Creating new collection with name {}'.format(request.form['new_collection']))
            # TODO: insert into collections table
            # TODO: update collection_id

        print('Adding image(s) to collection with id  {}'.format(collection_id))

        for file in request.files.getlist('files'):
            # TODO: insert into images table
            image_id = str(uuid.uuid1())
            s3upload(image_id, file)

    context = {}
    if 'patient_id' in session:
        context['patient_id'] = session['patient_id']

    # TODO: populate from database
    context['collections'] = [{'id': '1', 'name': 'Collection A'}, {'id': '2', 'name': 'Collection B'}]

    return render_template('upload.html', **context)

@app.route('/patient/<int:patient_id>/manage/', methods=['GET', 'POST'])
def manage_patient(patient_id):
    if request.method == 'POST':
        print('Deleting collection with id {}'.format(request.form['id']))
        # TODO: delete collection's images from S3 bucket
        # TODO: delete collection and images from database

    context = {}
    if 'patient_id' in session:
        context['patient_id'] = session['patient_id']

    # TODO: populate from database
    context['items'] = [{'id': '1', 'name': 'Collection A'}, {'id': '2', 'name': 'Collection B'}]

    return render_template('manage.html', **context)

@app.route('/manage/', methods=['GET', 'POST'])
def manage():
    if request.method == 'POST':
        print('Deleting patient with id {}'.format(request.form['id']))
        # TODO: delete patient's collections from S3 bucket
        # TODO: delete patient, collections, and images from database

    context = {}
    if 'patient_id' in session:
        context['patient_id'] = session['patient_id']

    # TODO: populate from database
    context['items'] = [{'id': '1', 'name': 'Patient A'}, {'id': '2', 'name': 'Patient B'}]

    return render_template('manage.html', **context)
