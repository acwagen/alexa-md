from alexamd_upload import app
from flask import Flask, render_template
from jinja2 import Template
from boto.s3.connection import S3Connection
import boto3
from botocore.errorfactory import ClientError

"""
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
"""
@app.route('/')
def index():
    return render_template('index.html')
