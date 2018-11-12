import os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'FIXME SET THIS WITH: $ python3 -c "import os; print(os.urandom(24))" '

S3_BUCKET = 'alexa-md-495'

DATABASE_FILENAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'alexa-md', 'var', 'alexamd.db'
)
