import flask
from alexamd_upload import app


class InvalidUsage(Exception):
    """Error handling class."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Classic init function."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """How to get the dictionary."""
        context = dict(self.payload or ())
        context['message'] = self.message
        context['status_code'] = self.status_code
        return context


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Actual error handler."""
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/api/v1/', methods=["GET"])
def patients():
    """Return all patients.

    Example:
    {
      "patient_id": 1,
      "name": "Patient Name",
      "collections_url": "/api/v1/p/1/collections/"
    },
    """
    #if "username" not in flask.session:
    #    raise InvalidUsage("Forbidden", status_code=403)

    context = { { 'patient_id': 1,
                  'name': 'Patient A',
                  'url': '/api/v1/p/1/collections/' },
                { 'patient_id': 2,
                  'name': 'Patient B',
                  'url': '/api/v1/p/2/collections/'
                }}

    # TODO: fetch patients from database

    return flask.jsonify(**context)


@app.route(
    '/api/v1/p/<int:patient_id>/collections/',
    methods=["GET"])
def collections(patient_id):
    """Return collections for patient_id.

    Example:
    {
      "patient_id": 1,
      "collection_id": 1,
      "collection_name": "Collection A",
      "first_img_url": "<s3 url>"
    }
    """
    #if "username" not in flask.session:
    #    raise InvalidUsage('Forbidden', status_code=403)

    context = { { 'patient_id': 1,
                  'collection_id': 1,
                  'collection_name': 'Collection A',
                  'first_img_url': 'https://www.puppyleaks.com/wp-content/uploads/2017/09/puppysmile.png' },
                { 'patient_id': 2,
                  'collection_id': 2,
                  'collection_name': 'Collection B',
                  'first_img_url': 'https://www.puppyleaks.com/wp-content/uploads/2017/09/puppysmile.png' }
              }

    # TODO: fetch collections from database

    return flask.jsonify(**context)
