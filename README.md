# Alexa MD

An Alexa skill to assist surgeons in navigating a file system in the operating room through voice commands.

## Getting Started

Follow the [steps to create an Alexa skill](https://developer.amazon.com/docs/devconsole/create-a-skill-and-choose-the-interaction-model.html#create-a-new-skill) and give the skill the name and invocation name 'file system.'

Select 'JSON Editor', open and save intents.json in the editor. Toggle 'Display Interface' under the Interfaces section. Build the model.

Navigate to the 'Endpoint' section of the Alexa Developer Console of the File System skill. Select the HTTPS button and paste the https ngrok url (from the directions below) into the 'Default Region' field. Select 'My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority', save the endpoint, and navigate to the Test tab. Start the skill with the invocation name, 'file system.'

### Prerequisites

Set up the environment with

```
pip install virtualenv
```

To install each subproject:

```
cd $subproject_folder
python -m virtualenv env
source env/bin/activate
pip install -e .
```

Initialize/reset the database (the same database will be used by each subproject):

```
cd alexa-md
./bin/alexamddb
```

In order to run Alexa MD through the Alexa Developer Console, [download ngrok](https://ngrok.com/download).

## AWS Configure

The images accessed within the apps are stored in an Amazon S3 bucket, which requires access and secret keys.
Download AWS Command line with:

```
sudo apt install awscli
```

And configure the settings with:

```
aws configure
```

Set the access and secret keys. The region input is us-east-2 and the format input is JSON.

## Running the web app (alexa-md-upload)

Navigate to the subproject folder and start the local Flask server with

```
cd alexa-md-upload
./bin/run
```

Once the app is running, go to http://localhost:5000/ in a browser.

## Running the skill (alexa-md)

Navigate to the subproject folder and start the local Flask server with

```
cd alexa-md
./bin/run
```

In a separate terminal, start the ngrok server with

```
./ngrok http 8000
```

Copy the url from the ngrok output and enter it as the skill's endpoint in the developer console as described above.

## Testing

After installation, run unit tests for each subproject with

```
cd $subproject_folder
python setup.py test
```

## Alexa MD User Guide
To start the system, say 'File System'.<br/>
To enter a certain directory or open an image, say 'Open {imagename}' or 'Open {imageindex}''.<br/>
To view the next or previous image, say 'Next {number}' or 'Previous {number}'.<br/>
To go back to the previous page, say 'Return'.<br/>
To ask for help with other commands, say 'Help'.<br/>
To exit the system, say 'Exit'.<br/>
