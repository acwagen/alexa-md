import unittest
from alexamd import app
from alexamd.ask import get_db, close_db
import os
import sqlite3
import json

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

    RESOURCES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')

    @classmethod
    def _execute_sql_script(cls, name):
        with app.app_context():
            cursor = get_db().cursor()

            filename = os.path.join(cls.RESOURCES_DIR, '{}.sql'.format(name))
            with open(filename, 'r') as sql:
                sqlscript = sql.read()
                cursor.executescript(sqlscript)

            cursor.close()
            close_db()

    @classmethod
    def setUpClass(cls):
        try:
            cls._execute_sql_script('drop')
        except sqlite3.OperationalError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            cls._execute_sql_script('drop')
        except sqlite3.OperationalError:
            pass

    def tearDown(self):
        AlexaMDTestBase._execute_sql_script('drop')

    def setUp(self):
        app.config['ASK_VERIFY_REQUESTS'] = False
        self.app = app.test_client()
        AlexaMDTestBase._execute_sql_script('create')
        AlexaMDTestBase._execute_sql_script('data')

    def test_example(self):
        response = self.app.post('/', data=json.dumps(self.launch))
        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
     unittest.main()
