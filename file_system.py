import logging, os
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from jinja2 import Template
from boto.s3.connection import S3Connection
import boto3

app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# global variables
my_list = []

def open_response(msg, index):
    s3 = boto3.client('s3')

    file_name = index + ".jpg"
    file_name = file_name.lower()

    url = s3.generate_presigned_url('get_object',Params={'Bucket':'alexa-md-495','Key':file_name,})
    parts = url.split('?')
    true_url = parts[0]

    return question(msg).display_render(title=index,  template='BodyTemplate7', image=true_url)



def start_response_s3(msg):    
    return question(msg).list_display_render(title='Welcome', template='ListTemplate2', listItems = my_list, hintText = 'Open 1')



@ask.launch
def launch():
    s3 = boto3.client('s3')
    resp = s3.list_objects_v2(Bucket='alexa-md-495')
    
    for obj in resp['Contents']:
        file_name = obj['Key']
        true_file_name = file_name.split('.')[0]
        url = s3.generate_presigned_url('get_object',Params={'Bucket':'alexa-md-495','Key':file_name,})
        parts = url.split('?')
        true_url = parts[0]
        item = {
            "token": "List-Item-0",
            "image": {
              "contentDescription": "XYZ 1",
              "sources": [
                {
                  "url": true_url
                }
              ]
            },
            "textContent": {
              "primaryText": {
                "text": true_file_name,
                "type": "RichText"
              },
              "secondaryText": None,
              "tertiaryText": None
            }
          }
        my_list.append(item)
    session.attributes['curr_index'] = -1
    return start()


@ask.intent("StartIntent")
def start():
    msg = render_template('welcome')
    return start_response_s3(msg)


@ask.intent("OpenIntent", mapping={'imageName': 'imageName'})
def open(imageName):
    filename = str(imageName)
    open_msg = render_template('open', filename=filename)

    for i in range(len(my_list)):
        if my_list[i]["textContent"]["primaryText"]["text"] == filename:
            session.attributes['curr_index'] = i
            break

    return open_response(open_msg, imageName)


@ask.intent("NextIntent", mapping={'number': 'number'})
def next(number):
    if session.attributes['curr_index'] == -1:
        return help()

    if not number:
        number = session.attributes['curr_index'] + 1 % len(my_list)
    else:
        number = int(number)
        number = session.attributes['curr_index'] + number % len(my_list)

    session.attributes['curr_index'] = number
    image_name = my_list[number]["textContent"]["primaryText"]["text"]
    next_msg = render_template('next', number=number)
    return open_response(next_msg, image_name)


@ask.intent("AMAZON.HelpIntent")
def help():
    # for now, when user ask help, the alexa will navigate the user to screen.
    # For Beta stage, with the help of session, the help info will be more
    # specific.
    help_msg = render_template('help')
    return question(help_msg).reprompt(help_msg)


if __name__ == '__main__':
    app.run(debug=True)
