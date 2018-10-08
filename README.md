# Alexa MD

An Alexa skill to assist surgeons in navigating a file system in the operating room through voice commands.

## Getting Started

Follow the [steps to create an Alexa skill](https://developer.amazon.com/docs/devconsole/create-a-skill-and-choose-the-interaction-model.html#create-a-new-skill) and give the skill the name and invocation name 'file system.'

Select 'JSON Editor' and open intents.json in the editor.

### Prerequisites

Install  with

```
pip install virtualenv
python -m virtualenv env
source env/bin/activate
pip install -e .
```
and [download ngrok](https://ngrok.com/download).


## Running the skill

Start the Flask server with

```
./bin/run
```

In a separate terminal, start the ngrok server with

```
ngrok.exe http 8000
```

Navigate to the 'Endpoint' section of the Alexa Developer Console of the File System skill. Select the HTTPS button and paste the https url given in the ngrok output into the 'Default Region' field. Select 'My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority', save the endpoint, and navigate to the Test tab. Start the skill with the invocation name, 'file system.'

## User Guide
To start the system, say 'File System'.<br/>
To view the home page, say 'Start' or 'Home'.<br/>
To view a certain image, say 'Open {imagename}'.<br/>
To go back to home page, say 'Return to Start/home'.<br/>
TO exit the system, say 'Goodbye'.<br/>
