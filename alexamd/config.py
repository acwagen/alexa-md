import os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'\x9dFeLQ5\x13\xbc\xe4\x88\x11)\x19\x14=\xbf\xd0\x94\x84ZaG\x91^'
SESSION_COOKIE_NAME = 'login'

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'alexamd.sqlite3'
)
