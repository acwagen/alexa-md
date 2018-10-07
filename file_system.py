import logging, os
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from jinja2 import Template

app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def placeholder_response(msg):
    import random
    img_url = random.choice([
        'https://img.purch.com/w/660/aHR0cDovL3d3dy5saXZlc2NpZW5jZS5jb20vaW1hZ2VzL2kvMDAwLzA4OC85MTEvb3JpZ2luYWwvZ29sZGVuLXJldHJpZXZlci1wdXBweS5qcGVn',
        'https://fortunedotcom.files.wordpress.com/2017/08/512536165-e1510081190643.jpg',
        'https://akc.org/wp-content/uploads/2015/10/Beagle-Puppies.jpg'
    ])

    return question(msg).display_render(title='Not implemented yet',  template='BodyTemplate6', background_image_url=img_url)


@ask.launch
def launch():
    return start()

@ask.intent("StartIntent")
def start():
    msg = render_template('welcome')
    return placeholder_response(msg)
    


@ask.intent("OpenIntent")
def open():
    filename = 'filename'
    open_msg = render_template('open', filename=filename)

    return placeholder_response(open_msg)


@ask.intent("AMAZON.HelpIntent")
def help():
    # for now, when user ask help, the alexa will navigate the user to screen.
    # For Beta stage, with the help of session, the help info will be more 
    # specific.
    help_msg = render_template('help')
    return question(help_msg).reprompt(help_msg)


if __name__ == '__main__':
    app.run(debug=True)
