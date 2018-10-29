import logging
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)

app.config.from_object('alexamd_upload.config')

# Tell our app about views.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
import alexamd_upload.views
