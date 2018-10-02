import logging, os
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

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

    return question(msg).standard_card(title='Oops',
        text='Not implemented yet!',
        large_image_url=img_url,
        small_image_url=img_url)


@ask.launch
def launch():
    welcome_msg = render_template('welcome')

    return placeholder_response(welcome_msg)


@ask.intent("StartIntent")
def start():
    return launch()


@ask.intent("OpenIntent")
def open():
    filename = 'filename'
    open_msg = render_template('open', filename=filename)

    return placeholder_response(open_msg)


@ask.intent("CloseIntent")
def close():
    filename = 'filename'
    close_msg = render_template('close', filename=filename)

    return placeholder_response(close_msg)


@ask.intent("PreviousIntent")
def previous():
    filename = 'previous_filename'
    previous_msg = render_template('open', filename=filename)

    return placeholder_response(previous_msg)


@ask.intent("NextIntent")
def next():
    filename = 'next_filename'
    next_msg = render_template('open', filename=filename)

    return placeholder_response(next_msg)


@ask.intent("HelpIntent")
def help():
    help_msg = render_template('help')

    return placeholder_response(help_msg)


@ask.intent("EndIntent")
def end():
    goodbye_msg = render_template('goodbye')

    return statement(goodbye_msg)


if __name__ == '__main__':
    app.run(debug=True)
