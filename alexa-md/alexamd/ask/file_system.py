from alexamd import app, ask
import flask
from flask import render_template
from flask_ask import Ask, statement,session, question
import flask_ask
from jinja2 import Template
from boto.s3.connection import S3Connection
import boto3
from botocore.errorfactory import ClientError
import sqlite3


conn = sqlite3.connect('alexamd.db')

# store cid to index id
cache = {}

def create_response(resp):
    resp._response.pop('shouldEndSession')

    if 'directives' not in resp._response:
        resp._response['directives'] = []
    resp._response['directives'].append({
      "type": "GameEngine.StartInputHandler",
      "timeout": 90000,
      "proxies": [],
      "recognizers": {},
      "events": {}
    })

    return resp

# global variables
#----------helper functions--------------------------------------------------

def dict_factory(cursor, row):
    output = {}
    for idx, col in enumerate(cursor.description):
        output[col[0]] = row[idx]
    return output

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

def disply_image_item(url, display_text):
    item = {
    "token": "List-Item-0",
    "image": {
        "contentDescription": "XYZ 1",
        "sources": [
            {
            "url": url
                }
            ]
        },
        "textContent": {
            "primaryText": {
                "text": display_text,
                "type": "RichText"
            },
            "secondaryText": None,
            "tertiaryText": None
        }
    }
    return item;


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
    Image_infos= []
    for cid in CIDS:
        row = db.execute('select IID from Images i where i.IND=0 and i.CID =?', (cid,)).fetchone()
        if row != None:
            Image_infos.append([row['IID'],cid])
    return Image_infos

# Return the IID next or prev
# if return result is None, the index is outofbound
def FetchScroll(CID, nextIndex):
    db = get_db()
    row = db.execute('select IID from Images where CID = ? and IND = ?',(CID,nextIndex,)).fetchone()
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
        return cur['PID']


def FetchCollectionNameByID(CID):
    db = get_db()
    cur = db.execute('select C_Name from Collections where CID=?',(CID,)).fetchone()
    return cur['C_Name']

def FetchCollectionID(PID,C_name,study):
    db = get_db()
    cur = db.execute('select CID from Collections where PID=? and C_name=? and Study=?',(PID,C_name,study)).fetchall()
    if (len(cur))==0:
        return None
    elif len(cur) > 1:
        return 'duplicate'
    else:
        return cur['CID']

def FetchFirstImageInCollection(CID):
    db = get_db()
    # check if we previously accessed an image in this collection
    if CID not in cache:
        cur = db.execute('select IID from Images where IND = 0 and CID=?',(CID,)).fetchone()
    else:
        cur = db.execute('select IID from Images where IND = ' + str(cache[CID]) + ' and CID=?',(CID,)).fetchone()
    return cur['IID']

def FetchPatientName(PID):
    db = get_db()
    cur = db.execute('select P_First, P_Last from Patients where PID=?',(PID,)).fetchone()
    return cur['P_Last']+','+cur['P_First']


def FetchImageCount(CID):
    db = get_db()
    cur = db.execute('select * from Images where CID=?',(CID,)).fetchall()
    return len(cur)


#-----------------------------------------------------------------------------
# S3 utility functions
def GetImageURL(image_name):
    # assume that image_name.jpg must exist in the S3 bucket
    s3 = boto3.client('s3')
    # image_name = image_name +".jpg"
    # don't need to manual add extention
    image_name = image_name.lower()
    s3.head_object(Bucket='alexa-md-495', Key=image_name)
    url = s3.generate_presigned_url('get_object',Params={'Bucket':'alexa-md-495','Key':image_name,})
    return [url.split('?')[0],image_name]
#------------------------------------------------------------------------------
#Navigate Functions

def NavigateToHome():
    db = get_db()
    cur = db.execute('select * from Patients')
    patent_info = cur.fetchall()
    patient_names = []
    for row in patent_info:
        patient_names.append(row['P_First'])
    msg = flask.render_template('welcome')
    return create_response(question(msg).list_display_render(title='Welcome', template='ListTemplate1', listItems = display_text_items(patient_names), hintText = 'Open 1'))


def NavigateToPatient(PID):

    patient_infos = FetchPatientsInfo(PID)
    display_texts = []
    all_studies = set()
    for info in patient_infos:
        if info[1] in all_studies:
            continue
        all_studies.add(info[1])
        display_texts.append(str(info[1]))

    msg = 'open patient page'
    path = GetCurrentPath()
    return create_response(question(msg).list_display_render(title=path, template='ListTemplate1', listItems = display_text_items(display_texts), hintText = 'Open 1'))


def NavigateToStudy(PID, study):
    patient_infos = FetchPatientsInfo(PID)
    CIDS = []
    for info in patient_infos:
        if info[1]==study:
            CIDS.append(info[0])
    if len(CIDS)==0:
        msg = 'This patient has no '+ study
        return create_response(question(msg))
    image_infos = FetchFirstImagesList(CIDS)
    display_items = []
    for info in image_infos:
        url = GetImageURL(info[0])[0] #url
        c_name = FetchCollectionNameByID(info[1])
        c_name = c_name
        image_count = FetchImageCount(info[1])
        c_name = "Collection Name: "+c_name + " , "+"Image Counts: "+str(image_count)
        display_items.append(disply_image_item(url,c_name))
    msg = 'Open study page'
    path = GetCurrentPath()
    return create_response(question(msg).list_display_render(title=path, template='ListTemplate2', listItems = display_items, hintText = 'Open 1'))


def NavigateToFirstImage(CID, PID):

    IID = FetchFirstImageInCollection(CID)
    url = GetImageURL(IID)[0]
    # patient_name = FetchPatientName(PID)
    msg = 'open image'
    path = GetCurrentPath()
    return create_response(question(msg).display_render(title=path,  template='BodyTemplate7', image=url))

def NavigateToImage(CID, Index, PID,help_msg = None):
    cache[CID] = Index
    IID = FetchScroll(CID, Index)
    url = GetImageURL(IID)[0]
    msg = 'open image'
    # patient_name = FetchPatientName(PID)
    if help_msg != None:
        msg = help_msg
    path = GetCurrentPath()
    return create_response(question(msg).display_render(title=path,  template='BodyTemplate7', image=url))





 #---------------------------------------------------------------------

#functions that transfer Display ID into PID, CID

def GetPidFromDisplayID(display_id):
    db = get_db()
    cur = db.execute('select * from Patients')
    patent_info = cur.fetchall()

    if display_id >= len(patent_info):
        return None
    else:
        return str(patent_info[display_id]['PID'])

def GetStudyFromDisplayID(display_id, PID):
    patient_infos = FetchPatientsInfo(PID)
    if display_id >= len(patient_infos):
        return None
    else:
        return patient_infos[display_id][1]

def GetCidFromDisplayID(display_id, PID, study):
    patient_infos = FetchPatientsInfo(PID)
    CIDS = []
    for info in patient_infos:
        if info[1]==study:
            CIDS.append(info[0])
    if len(CIDS)==0:
        return None
    image_infos = FetchFirstImagesList(CIDS)
    if display_id >= len(image_infos):
        return None
    return str(image_infos[display_id][1])


def GetCurrentPath():
    if session.attributes['level'] == 'patient':
        res = "Patient: "+FetchPatientName(session.attributes['patient'])
        return res
    elif session.attributes['level'] == 'study':
        res = "Patient: "+FetchPatientName(session.attributes['patient'])
        res += " | Study: "+ session.attributes['study']
        return res
    elif session.attributes['level']== 'image':
        res = "Patient: "+FetchPatientName(session.attributes['patient'])
        res += " | Study: "+ session.attributes['study']
        res += " | Collection: "+ FetchCollectionNameByID(session.attributes['collection'])
        res += " | Index: "+ str(session.attributes['index'])
        return res

    else:
        print("Level name is invalid")
        return None



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
       return create_response(question(msg).display_render(title=filename,  template='BodyTemplate7', image=true_url))
    except ClientError:
      retry_message = 'There is no '+ filename +' in the file system, please retry'
      return create_response(question(retry_message).reprompt(retry_message))


@ask.launch
def launch():
    print('launch')
    session.attributes['level'] = 'home'
    # session.attributes['patient'] = None
    # session.attributes['study'] = None
    # session.attributes['collection'] = None
    # session.attributes['index'] = None
    print(session.attributes)
    return NavigateToHome()


@ask.intent("StartIntent")
def start():
    # msg = render_template('welcome')
    # session.attributes.attributes['curr_index'] = -1
    # return start_response_s3(msg)
    print("running start")
    session.attributes['level'] = 'home'
    session.attributes['patient'] = None
    session.attributes['study'] = None
    session.attributes['collection'] = None
    session.attributes['index'] = None
    return NavigateToHome()

@ask.intent("OpenIntent", mapping={'imageIndex': 'imageIndex'})
def open(imageIndex):
    print(imageIndex)
    useID = True
    try:
        imageIndex = int(imageIndex)
        # it's a number
        filename = str(imageIndex)
    except ValueError:
        # it's a string like 'Mike'
        useID = False
        filename = str(imageIndex)

    print('Open')

    if session.attributes['level']=='home':

        if useID:

            display_id = int(filename)-1
            pid = GetPidFromDisplayID(display_id)
            if pid == None:
                return create_response(question('out of bound, please retry'))
            print('PID is ' + pid)
            session.attributes['patient'] = pid # set the current Patient
            session.attributes['level'] = 'patient'
            return NavigateToPatient(session.attributes['patient'])
        else:
            PID = FetchPatientByFirstName(filename)
            if PID == None:
                msg = 'Please try another name'
                return create_response(question(msg))
            elif PID == 'duplicate':
                msg = 'There are more than ' + filename + ' in the file system'
                return create_response(question(msg))
            else:
                session.attributes['patient'] = PID
                session.attributes['level'] = 'patient'
                return NavigateToPatient(session.attributes['patient'])

    elif session.attributes['level'] == 'patient':
        # if not string, filename = cid. if string, filename = study
        if useID:
            display_id = int(filename)-1
            study = GetStudyFromDisplayID(display_id,session.attributes['patient'])
            if study == None:
                return create_response(question('out of bound, please retry'))

            print('Study is ' + study)
            session.attributes['study'] = study
            session.attributes['level'] = 'study'
            return NavigateToStudy(session.attributes['patient'],session.attributes['study'])
        else:
            session.attributes['study'] = filename
            session.attributes['level'] = 'study'
            return NavigateToStudy(session.attributes['patient'],session.attributes['study'])
    elif session.attributes['level'] == 'study':
        if useID:
            display_id = int(filename)-1
            CID = GetCidFromDisplayID(display_id,session.attributes['patient'],session.attributes['study'])
            if CID == None:
                return create_response(question('out of bound, please retry'))
            print('CID is '+CID)
            session.attributes['collection'] = CID
            session.attributes['index'] = 0
            session.attributes['level'] = 'image'
            return NavigateToFirstImage(session.attributes['collection'],session.attributes['patient'])
        else:
            CID = FetchCollectionID(session.attributes['patient'],filename,session.attributes['study'])
            session.attributes['collection'] = CID
            session.attributes['index'] = 0
            session.attributes['level'] = 'image'
            return NavigateToFirstImage(session.attributes['collection'],session.attributes['patient'])
    elif session.attributes['level'] == 'image':
        msg = "You should not call open in this stage, try another command"
        return create_response(question(msg))
    else:
        # should not happen
        print("this should not happen")
        print(session.attributes['level'])
        exit(1)


@ask.intent("ReturnIntent")
def returndir():

    if session.attributes['level']=='home' or session.attributes['level'] == 'patient':
        # goes back to home level and resets patient
        session.attributes['level'] = 'home'
        session.attributes['patient'] = None

        # displays list of patients
        return launch()

    elif session.attributes['level'] == 'study':
        # goes back one session.attributes level and resets study
        session.attributes['level'] = 'patient'
        session.attributes['study'] = None

        # displays studies of current patient
        return NavigateToPatient(session.attributes['patient'])

    elif session.attributes['level'] == 'image':
        # goes back one session.attributes level and resets collection
        session.attributes['level'] = 'study'
        session.attributes['collection'] = None

        # display collections of current study of current patient
        return NavigateToStudy(session.attributes['patient'],session.attributes['study'])

    else:
        # should not happen
        print("this should not happen")
        print(session.attributes['level'])
        exit(1)


@ask.intent("NextIntent", mapping={'number': 'number'})
def next(number):
    # get nextIndex
    if session.attributes['level'] != 'image':
        return error()
    session.attributes['index'] += int(number)
    item = FetchScroll(session.attributes['collection'], session.attributes['index'])
    if item == None:
        help_msg = 'Moving ' + str(number)+" spaces forward went out of bounds. Can't go next"
        session.attributes['index'] -= int(number)
        return NavigateToImage(session.attributes['collection'], session.attributes['index'],session.attributes['patient'], help_msg)
    else:
        return NavigateToImage(session.attributes['collection'], session.attributes['index'],session.attributes['patient'])

@ask.intent("AMAZON.NextIntent")
def nextOne():
    # get nextIndex
    next(1)
    # if session.attributes['level'] != 'image':
    #     return error()

    # session.attributes['index'] += 1
    # item = FetchScroll(session.attributes['collection'], session.attributes['index'])
    # if item == None:
    #     help_msg = "Moving 1 space forward went out of bounds. Can't go next"
    #     session.attributes['index'] -= 1
    #     return NavigateToImage(session.attributes['collection'], session.attributes['index'], session.attributes['patient'],help_msg)
    # else:
    #     return NavigateToImage(session.attributes['collection'], session.attributes['index'],session.attributes['patient'])


@ask.intent("AMAZON.ScrollDownIntent")
def ScrollDownOne():
    next(1)


@ask.intent("PreviousIntent", mapping={'number': 'number'})
def previous(number):
    # get nextIndex
    if session.attributes['level'] != 'image':
        return error()
    session.attributes['index'] -= int(number)
    item = FetchScroll(session.attributes['collection'], session.attributes['index'])
    if item == None:
        help_msg = "Moving " + str(number)+" spaces backward went out of bounds. Can't go to previous"
        session.attributes['index'] += int(number)
        return NavigateToImage(session.attributes['collection'], session.attributes['index'], session.attributes['patient'],help_msg)
    else:
        return NavigateToImage(session.attributes['collection'], session.attributes['index'],session.attributes['patient'])


@ask.intent("AMAZON.PreviousIntent")
def previousOne():
    # get nextIndex
    previous(1)
    # if session.attributes['level'] != 'image':
    #     return error()
    # session.attributes['index'] -= 1
    # item = FetchScroll(session.attributes['collection'], session.attributes['index'])
    # if item == None:
    #     help_msg = "Moving 1 space backward went out of bounds. Can't go to previous"
    #     session.attributes['index'] += 1
    #     return NavigateToImage(session.attributes['collection'], session.attributes['index'],session.attributes['patient'], help_msg)
    # else:
    #     return NavigateToImage(session.attributes['collection'], session.attributes['index'],session.attributes['patient'])


@ask.intent("AMAZON.ScrollUpIntent")
def scrollUpOne():
    previous(1)


@ask.intent("AMAZON.HelpIntent")
def help():
    # for now, when user ask help, the alexa will navigate the user to screen.
    # For Beta stage, with the help of session.attributes, the help info will be more
    # specific.
    help_msg = render_template('help')
    return create_response(question(help_msg))
    # if session.attributes.attributes['curr_index'] == -1:
    #     return start_response_s3(help_msg)
    # else:
    #     image_name = my_list[session.attributes.attributes['curr_index']]["textContent"]["primaryText"]["text"]
    #     return open_response(help_msg, image_name)

def error():

    error_msg = render_template('error')
    return create_response(question(error_msg))
