from alexamd import app, ask
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from jinja2 import Template
from boto.s3.connection import S3Connection
import boto3
from botocore.errorfactory import ClientError
import sqlite3


conn = sqlite3.connect('alexamd.db')

# global variables

def get_db():
    if not hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db = sqlite3.connect(
            'var/alexamd.db')
        flask.g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db

def close_db():
    if hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db.commit()
        flask.g.sqlite_db.close()


def display_text_items(names):
    res = []
    for name in names:
        item = {
            "token": "List-Item-0",
            "textContent": {
                "primaryText": {
                    "text": name,
                    "type": "RichText"
                },
                "secondaryText": None,
                "tertiaryText": None
            }
        }
        res.append(item)
    return res

#-----------------------------------------------------------------------------
# The functions below are SQL execution that will be used in the intents

# Return the names of studys that this patient has.
# Used in Patient Page
 #return list of tuples (CID, study)
def FetchPatientsInfo(PID):
   
    db = get_db()
    cur = db.execute('select CID,Study from Collections where PID = ?', (PID,))
    res = []
    for row in cur.fetchall():
        res.append([row['CID'], row['Study']])
    return res

# Return the IID of all the first image in a study
# Used in collections page
def FetchFirstImagesList(CIDS):
    db = get_db()
    Image_names = []
    for cid in CIDS:
        row = db.execute('select IID from Images i where i.IND=0 and i.CID =?', (cid,)).fetechone()
        if row != None:
            Image_names.append(row[IID])
    return Image_names

# Return the IID next or prev
# if return result is None, the index is outofbound
def FetchScroll(CID, nextIndex):
    db = get_db()
    row = db.execute('select IID from Images where CID = ? and IND = ?',(CID,nextIndex,)).fetechone()
    if row== None:
        return None
    else:
        return row['IID']

#return the PID of the Patinet if Patient's First name is unique
def FetchPatientByFirstName(name):
    # if return None, there is no such patient
    # if return Duplicate, there is more than one patient with the same name
    db = get_db()
    cur = db.execute('select PID from Patients where P_First = ?', (name,)).fetchall()
    if len(cur) == 0:
        return None
    elif len(cur) > 1:
        return 'duplicate'
    else:
        return cur[PID]


#-----------------------------------------------------------------------------
# S3 utility functions
def GetImageURL(image_name):
    # assume that image_name.jpg must exist in the S3 bucket
    s3 = boto.client('s3')
    image_name = image_name +".jpg"
    image_name = image_name.lower()
    s3.head_object(Bucket='alexa-md-495', Key=image_name)
    url = s3.generate_presigned_url('get_object',Params={'Bucket':'alexa-md-495','Key':image_name,})
    return url.split('?')[0]
#------------------------------------------------------------------------------

    



# fucntions to implement the skills.

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



def scroll(number):
    if session.attributes['curr_index'] == -1:
        return help()
    
    last_index = len(my_list) - 1

    if not number:
        number = 1
    else:
        number = int(number)
    
    if session.attributes['curr_index'] + number > last_index:
        session.attributes['curr_index'] = last_index
        msg = "You're at the end of the folder."
        image_name = my_list[last_index]["textContent"]["primaryText"]["text"]
        return open_response(msg, image_name)
    
    if session.attributes['curr_index'] + number < 0:
        session.attributes['curr_index'] = 0
        msg = "You're at the beginning of the folder."
        image_name = my_list[0]["textContent"]["primaryText"]["text"]
        return open_response(msg, image_name)

    session.attributes['curr_index'] += number
    image_name = my_list[session.attributes['curr_index']]["textContent"]["primaryText"]["text"]
    if number > 0:
        msg = render_template('next', number=number)
    else:
        number *= -1
        msg = render_template('previous', number=number)
    return open_response(msg, image_name)



@ask.launch
def launch():

    # s3 = boto3.client('s3')
    # resp = s3.list_objects_v2(Bucket='alexa-md-495')

    # for obj in resp['Contents']:
    #     file_name = obj['Key']
    #     true_file_name = file_name.split('.')[0]
    #     url = s3.generate_presigned_url('get_object',Params={'Bucket':'alexa-md-495','Key':file_name,})
    #     parts = url.split('?')
    #     true_url = parts[0]
    #     item = {
    #         "token": "List-Item-0",
    #         "image": {
    #           "contentDescription": "XYZ 1",
    #           "sources": [
    #             {
    #               "url": true_url
    #             }
    #           ]
    #         },
    #         "textContent": {
    #           "primaryText": {
    #             "text": true_file_name,
    #             "type": "RichText"
    #           },
    #           "secondaryText": None,
    #           "tertiaryText": None
    #         }
    #       }
    #     my_list.append(item)
    # session.attributes['curr_index'] = -1
    db = get_db()
    cur = db.execute('select * from Patients')
    patent_info = cur.fetchall()
    patient_names = []
    for row in patent_info:
        patient_names.append("Patient: "+row['PID'])

    msg = render_template('welcome')
    session['level'] = 'home'
    return question(msg).list_display_render(title='Welcome', template='ListTemplate1', listItems = display_text_items(patient_names), hintText = 'Open 1')


@ask.intent("StartIntent")
def start():
    # msg = render_template('welcome')
    # session.attributes['curr_index'] = -1
    # return start_response_s3(msg)
    launch()


@ask.intent("OpenIntent", mapping={'imageName': 'imageName'})
def open(imageName):
    try:
        imageName = int(imageName)
        # it's a number
        filename = str(my_list[imageName - 1]["textContent"]["primaryText"]["text"])
    except ValueError:
        # it's a string like 'Mike'
        filename = str(imageName)
    if session['level']=='home':
        

    elif session['level'] == 'patient':

    elif session['level'] == 'study':
    
    elif session['level'] == 'image':
    
    else:
        exit(1)

    # open_msg = render_template('open', filename=filename)

    # # initialize current index variable in flask session
    # for i in range(len(my_list)):
    #     if my_list[i]["textContent"]["primaryText"]["text"] == filename.lower():
    #         session.attributes['curr_index'] = i
    #         break

    # return open_response(open_msg, filename)


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

    return scroll(number)


@ask.intent("AMAZON.NextIntent")
def nextOne():
    if session.attributes['curr_index'] == -1:
        return help()


    last_index = len(my_list) - 1
    
    if session.attributes['curr_index'] == last_index:
        help_msg = "Cannot go next. You're already at the end."
        image_name = my_list[last_index]["textContent"]["primaryText"]["text"]
        return open_response(help_msg, image_name)
    
    return scroll(1)


@ask.intent("PreviousIntent", mapping={'number': 'number'})
def previous(number):
    if session.attributes['curr_index'] == -1:
        return help()
    
    last_index = len(my_list) - 1

    if not number:
        number = -1
    else:
        number = int(number) * -1
    
    if session.attributes['curr_index'] == 0:
        help_msg = "Cannot go previous. You're already at the front."
        image_name = my_list[0]["textContent"]["primaryText"]["text"]
        return open_response(help_msg, image_name)

    return scroll(number)


@ask.intent("AMAZON.PreviousIntent")
def previousOne():
    if session.attributes['curr_index'] == -1:
        return help()
    
    if session.attributes['curr_index'] == 0:
        help_msg = "Cannot go previous. You're already at the front."
        image_name = my_list[0]["textContent"]["primaryText"]["text"]
        return open_response(help_msg, image_name)

    return scroll(-1)


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
