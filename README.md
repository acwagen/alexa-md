# Alexa MD

An Alexa skill to assist surgeons in navigating a file system in the operating room through voice commands.

## Getting Started

Follow the [steps to create an Alexa skill](https://developer.amazon.com/docs/devconsole/create-a-skill-and-choose-the-interaction-model.html#create-a-new-skill) and give the skill the name and invocation name 'file system.'

Select 'JSON Editor', open and save intents.json in the editor. Toggle 'Display Interface' under the Interfaces section. Build the model.

Running the skill locally is optional. To run with the deployed app, follow the instructions below to set the skill's endpoint, and enter https://e73a546c.ngrok.io/ for the url.

Navigate to the 'Endpoint' section of the Alexa Developer Console of the File System skill. Select the HTTPS button and paste the https ngrok url into the 'Default Region' field. Select 'My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority', save the endpoint, and navigate to the Test tab. Start the skill with the invocation name, 'file system.'

### Prerequisites

To install and run locally, install  with

```
pip install virtualenv
python -m virtualenv env
source env/bin/activate
pip install -e .
```
and [download ngrok](https://ngrok.com/download).

## AWS Configure

The images accessed with this skill are stored in Amazon S3 buckets, which require access and secret keys.
Download AWS Command line with:

```
sudo apt install awscli
```

And configure your settings with:

```
aws configure
```

Set your access and secret keys to the ones we sent to you. For the last two inputs, the region is us-east-2 and format is JSON.

## Running the skill

Start the local Flask server with

```
./bin/run
```

In a separate terminal, start the ngrok server with

```
./ngrok http 8000
```

Copy the url from the ngrok output and enter it as the skill's endpoint in the developer console as described above.

## User Guide
To start the system, say 'File System'.<br/>
To view a certain image, say 'Open {imagename}' or 'Open {imageindex}.<br/>
To view the next image, say 'Next {number}.<br/>
To go back to home page, say 'Return to Start/home'.<br/>
To ask for help with other commands, say 'Help'.<br/>
To exit the system, say 'Exit'.<br/>
