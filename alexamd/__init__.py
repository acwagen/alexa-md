import logging
import flask
import flask_ask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)
ask = flask_ask.Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# Read settings from config module (insta485/config.py)
app.config.from_object('alexamd.config')

# Overlay settings read from file specified by environment variable. This is
# useful for using different on development and production machines.
# Reference: http://flask.pocoo.org/docs/0.12/config/
app.config.from_envvar('ALEXAMD_SETTINGS', silent=True)

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
import alexamd.views
import alexamd.model
