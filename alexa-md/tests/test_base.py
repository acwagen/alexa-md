"""
Smoke test using the samples.
"""

import unittest
from alexamd import app
from requests import post

class AlexaMDTestBase(unittest.TestCase):
    launch = {
      "version": "1.0",
      "session": {
        "new": True,
        "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
        "application": {
          "applicationId": "fake-application-id"
        },
        "attributes": {},
        "user": {
          "userId": "amzn1.account.AM3B00000000000000000000000"
        }
      },
      "context": {
        "System": {
          "application": {
            "applicationId": "fake-application-id"
          },
          "user": {
            "userId": "amzn1.account.AM3B00000000000000000000000"
          },
          "device": {
            "supportedInterfaces": {
              "AudioPlayer": {}
            }
          }
        },
        "AudioPlayer": {
          "offsetInMilliseconds": 0,
          "playerActivity": "IDLE"
        }
      },
      "request": {
        "type": "LaunchRequest",
        "requestId": "string",
        "timestamp": "string",
        "locale": "string",
        "intent": {
          "name": "TestPlay",
          "slots": {
            }
          }
        }
    }

    def setUp(self):
        app.config['ASK_VERIFY_REQUESTS'] = False
        self.app = app.test_client()

    def test_example(self):
        response = self.app.post('/', json=self.launch)
        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
     unittest.main()
