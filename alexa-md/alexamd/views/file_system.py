from alexamd import app, ask
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from jinja2 import Template
from boto.s3.connection import S3Connection
import boto3
from botocore.errorfactory import ClientError


# global variables
my_list = []

def open_response(msg, filename):
    s3 = boto3.client('s3')

    file_name = filename + ".jpg"
    file_name = file_name.lower()

    try:
       s3.head_object(Bucket='alexa-md-495', Key=file_name)
       url = s3.generate_presigned_url('get_object',Params={'Bucket':'alexa-md-495','Key':file_name,})
       parts = url.split('?')
       true_url = parts[0]
       return question(msg).display_render(title=filename,  template='BodyTemplate7', image=true_url)
    except ClientError:
      retry_message = 'There is no '+ filename +' in the file system, please retry'
      return question(retry_message).reprompt(retry_message)



def start_response_s3(msg):
    return question(msg).list_display_render(title='Welcome', template='ListTemplate2', listItems = my_list, hintText = 'Open 1')



@ask.launch
def launch():
    del my_list[:]
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
    session.attributes['curr_index'] = -1
    return start_response_s3(msg)


@ask.intent("OpenIntent", mapping={'imageName': 'imageName'})
def open(imageName):
    try:
        imageName = int(imageName)
        # it's a number
        filename = str(my_list[imageName - 1]["textContent"]["primaryText"]["text"])
    except ValueError:
        # it's a string like 'Mike'
        filename = str(imageName)

    open_msg = render_template('open', filename=filename)

    # initialize current index variable in flask session
    for i in range(len(my_list)):
        if my_list[i]["textContent"]["primaryText"]["text"] == filename.lower():
            session.attributes['curr_index'] = i
            break

    return open_response(open_msg, filename)


@ask.intent("NextIntent", mapping={'number': 'number'})
def next(number):
    if session.attributes['curr_index'] == -1:
        return help()
    
    last_index = len(my_list) - 1

    if not number:
        number = 1
    else:
        number = int(number)
    
    if session.attributes['curr_index'] == last_index:
        help_msg = "Cannot go next. You're already at the end."
        image_name = my_list[last_index]["textContent"]["primaryText"]["text"]
        return open_response(help_msg, image_name)
    if session.attributes['curr_index'] + number > last_index:
        session.attributes['curr_index'] = last_index
        msg = "You're at the end of the folder."
        image_name = my_list[last_index]["textContent"]["primaryText"]["text"]
        return open_response(msg, image_name)

    session.attributes['curr_index'] += number
    image_name = my_list[session.attributes['curr_index']]["textContent"]["primaryText"]["text"]
    next_msg = render_template('next', number=number)
    return open_response(next_msg, image_name)


@ask.intent("AdjustScreenIntent")
def AdjustScreen():
    # only used for the home page right now. Different from scroll
    return question("Adjust Screen").list_display_render(title='Welcome', template='ListTemplate2', listItems = my_list, hintText = 'Open 1')



@ask.intent("AMAZON.HelpIntent")
def help():
    # for now, when user ask help, the alexa will navigate the user to screen.
    # For Beta stage, with the help of session, the help info will be more
    # specific.
    help_msg = render_template('help')
    if session.attributes['curr_index'] == -1:
        return start_response_s3(help_msg)
    else:
        image_name = my_list[session.attributes['curr_index']]["textContent"]["primaryText"]["text"]
        return open_response(help_msg, image_name)
