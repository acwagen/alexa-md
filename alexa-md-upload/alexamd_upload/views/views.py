from alexamd_upload import app
from flask import render_template, request
from s3utils import s3upload

@app.route('/')
def index():
    context = {}
    return render_template('index.html', **context)

@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # TODO: add support for multiple file uploads
        s3upload(request.files['files'])

    return render_template('upload.html')

@app.route('/manage/', methods=['GET', 'POST'])
def manage():
    if request.method == 'POST':
        print('Not implemented yet')

    context = {}
    return render_template('todo.html', **context)
