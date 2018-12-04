import unittest
from alexamd import app
from alexamd.ask import get_db, close_db
import os
import sqlite3
import json


class AlexaMDTestBase(unittest.TestCase):

    RESOURCES_DIR = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'resources')

    def _execute_sql_command(self, cmd):
        with app.app_context():
            cursor = get_db().cursor()
            cursor.execute(cmd)
            cursor.close()
            close_db()


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

    def getListItemsFromResponse(self, response):
        list_items = []
        response_list_items = response['response']['directives'][0]['template']['listItems']
        for item in response_list_items:
            list_items.append(item['textContent']['primaryText']['text'])
        return list_items

    def getSessionAttributesFromResponse(self, response):
        return response['sessionAttributes']

    def openIntent(self, value, session_attributes=None):
        with open(os.path.join(self.RESOURCES_DIR, 'open.json'), 'r') as json_data:
            data = json.load(json_data)
            data['request']['intent']['slots']['imageIndex']['value'] = value
            if session_attributes:
                data['session']['attributes'] = session_attributes
            return json.dumps(data)


if __name__ == "__main__":
    unittest.main()
