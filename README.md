# Alexa MD

An Alexa skill to assist surgeons in navigating a file system in the operating room through voice commands.

## Getting Started

Follow the [steps to create an Alexa skill](https://developer.amazon.com/docs/devconsole/create-a-skill-and-choose-the-interaction-model.html#create-a-new-skill) and give the skill the name and invocation name 'file system.'

Select 'JSON Editor' and open intents.json in the editor.

### Prerequisites

Install flask-ask with

```
pip install flask-ask
```
and [download ngrok](https://ngrok.com/download).


## Running the skill

Start the Flask server with

```
python file_system.py
```

In a separate terminal, start the ngrok server with

```
ngrok.exe http 5000
```

Navigate to the 'Endpoint' section of the Alexa Developer Console of the File System skill. Select the HTTPS button and paste the https url given in the ngrok output into the 'Default Region' field. Select 'My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority', save the endpoint, and navigate to the Test tab. Start the skill with the invocation name, 'file system.'

## User Guide
To start the system, say 'File System'.\n
To view the home page, say 'Start' or 'Home'.\n
To view a certain image, say 'Open {imagename}'.\n
To go back to home page, say 'Return to Start/home'.\n
TO exit the system, say 'Goodbye'.\n

## Other

If running the app results in the error `module lib has no attribute x509v3_ext_get`, run
```pip install 'cryptography<2.2'```.
