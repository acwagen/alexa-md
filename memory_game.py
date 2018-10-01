import logging

from random import randint

from flask import Flask, render_template, send_file

from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@app.route('/img')
def get_image():
    filename = 'puppy.jpg'
    return send_file(filename, mimetype='image/jpeg')

@app.route('/test')
def index():
    context = {}
    return render_template('index.html', **context)

@ask.launch

def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("YesIntent")

def next_round():

    numbers = [randint(0, 9) for _ in range(3)]

    round_msg = render_template('round', numbers=numbers)

    session.attributes['numbers'] = numbers[::-1]  # reverse

    return question(round_msg)


@ask.intent("NoIntent")

def quit_game():

    goodbye_msg = render_template('goodbye')

    return statement(goodbye_msg).standard_card(title='Goodbye...', large_image_url='https://eed2445f.ngrok.io/img')
    # large_image_url='https://img.purch.com/w/660/aHR0cDovL3d3dy5saXZlc2NpZW5jZS5jb20vaW1hZ2VzL2kvMDAwLzA4OC85MTEvb3JpZ2luYWwvZ29sZGVuLXJldHJpZXZlci1wdXBweS5qcGVn')

@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})

def answer(first, second, third):

    winning_numbers = session.attributes['numbers']

    if [first, second, third] == winning_numbers:

        msg = render_template('win')

    else:

        msg = render_template('lose')

    return question(msg)


if __name__ == '__main__':

    app.run(debug=True)
