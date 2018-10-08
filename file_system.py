import logging, os
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from jinja2 import Template

app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def placeholder_response(msg, index):
    # import random
    # img_url = random.choice([
    #     'https://img.purch.com/w/660/aHR0cDovL3d3dy5saXZlc2NpZW5jZS5jb20vaW1hZ2VzL2kvMDAwLzA4OC85MTEvb3JpZ2luYWwvZ29sZGVuLXJldHJpZXZlci1wdXBweS5qcGVn',
    #     'https://fortunedotcom.files.wordpress.com/2017/08/512536165-e1510081190643.jpg',
    #     'https://akc.org/wp-content/uploads/2015/10/Beagle-Puppies.jpg'
    # ])

    # return question(msg).display_render(title='Not implemented yet',  template='BodyTemplate6', background_image_url=img_url)

    print("INDEX NUMBER IS: ", index)

    if index == '1':
        img_url = 'https://img.purch.com/w/660/aHR0cDovL3d3dy5saXZlc2NpZW5jZS5jb20vaW1hZ2VzL2kvMDAwLzA4OC85MTEvb3JpZ2luYWwvZ29sZGVuLXJldHJpZXZlci1wdXBweS5qcGVn'
    elif index == '2':
        img_url = 'https://fortunedotcom.files.wordpress.com/2017/08/512536165-e1510081190643.jpg'
    elif index == '3':
        img_url = 'https://akc.org/wp-content/uploads/2015/10/Beagle-Puppies.jpg'
    else:
        img_url = 'https://j3uv01gyifh3iqdfjuwz0qip-wpengine.netdna-ssl.com/wp-content/uploads/2017/06/puppy.jpg'

    return question(msg).display_render(title='Not implemented yet',  template='BodyTemplate6', background_image_url=img_url)



def start_response(msg):
    img_url1 = "https://img.purch.com/w/660/aHR0cDovL3d3dy5saXZlc2NpZW5jZS5jb20vaW1hZ2VzL2kvMDAwLzA4OC85MTEvb3JpZ2luYWwvZ29sZGVuLXJldHJpZXZlci1wdXBweS5qcGVn"
    img_url2 = 'https://fortunedotcom.files.wordpress.com/2017/08/512536165-e1510081190643.jpg'
    img_url3 = 'https://akc.org/wp-content/uploads/2015/10/Beagle-Puppies.jpg'
    item1 = {
            "token": "List-Item-0",
            "image": {
              "contentDescription": "XYZ 1",
              "sources": [
                {
                  "url": img_url1
                }
              ]
            },
            "textContent": {
              "primaryText": {
                "text": "Pupper",
                "type": "PlainText"
              },
              "secondaryText": None,
              "tertiaryText": None
            }
          }
    item2 = {
            "token": "List-Item-1",
            "image": {
              "contentDescription": "Sleepy Boi",
              "sources": [
                {
                  "url": img_url2
                }
              ]
            },
            "textContent": {
              "primaryText": {
                "text": "Sleepy Boi",
                "type": "PlainText"
              },
              "secondaryText": None,
              "tertiaryText": None
            }
          }
    item3 = {
            "token": "List-Item-2",
            "image": {
              "contentDescription": "XYZ 3",
              "sources": [
                {
                  "url": img_url3
                }
              ]
            },
            "textContent": {
              "primaryText": {
                "text": "Puppers",
                "type": "PlainText"
              },
              "secondaryText": None,
              "tertiaryText": None
            }
          }
    my_list = [item1, item2, item3]
    return question(msg).list_display_render(title='Welcome', template='ListTemplate2', listItems = my_list, hintText = 'Open 1')

@ask.launch
def launch():
    return start()

@ask.intent("StartIntent")
def start():
    msg = render_template('welcome')
    return start_response(msg)
    


@ask.intent("OpenIntent", mapping={'imageIndex': 'imageIndex'})
def open(imageIndex):
    filename = 'filename'
    open_msg = render_template('open', filename=filename)

    return placeholder_response(open_msg, imageIndex)


@ask.intent("HelpIntent")
def help():
    # for now, when user ask help, the alexa will navigate the user to screen.
    # For Beta stage, with the help of session, the help info will be more 
    # specific.
    help_msg = render_template('help')
    return question(help_msg).reprompt(help_msg)


if __name__ == '__main__':
    app.run(debug=True)
