import logging
import flask
import flask_ask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)
ask = flask_ask.Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# Tell our app about views.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
import alexamd.ask
