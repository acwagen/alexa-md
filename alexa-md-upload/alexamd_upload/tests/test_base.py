import unittest
from alexamd_upload import app, model
import requests
import bs4
import os
import sqlite3

class TestAlexaMDUploadBase(unittest.TestCase):
    RESOURCES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')

    @classmethod
    def _execute_sql_script(cls, name):
        with app.app_context():
            cursor = model.get_db().cursor()

            filename = os.path.join(cls.RESOURCES_DIR, '{}.sql'.format(name))
            with open(filename, 'r') as sql:
                sqlscript = sql.read()
                cursor.executescript(sqlscript)

            cursor.close()

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

    def setUp(self):
        self.app = app.test_client()
        TestAlexaMDUploadBase._execute_sql_script('create')
        TestAlexaMDUploadBase._execute_sql_script('data')

    def tearDown(self):
        TestAlexaMDUploadBase._execute_sql_script('drop')

    def assertOptions(self, url, option_values, selected=None):
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

        soup = bs4.BeautifulSoup(response.data, "html.parser")
        options = soup.find_all('option')
        self.assertEqual(len(options), len(option_values))
        for option in options:
            id = int(option.get('value'))
            name = option.text
            self.assertIn(id, option_values)
            self.assertEqual(name, option_values[id])

        selected_options = soup.find_all('option', selected=True)
        if selected:
            self.assertEqual(len(selected_options), 1)
            self.assertEqual(int(selected_options[0].get('value')), selected)

    def assertListItems(self, url, list_values):
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

        soup = bs4.BeautifulSoup(response.data, "html.parser")
        list_items = soup.find_all('li')
        self.assertEqual(len(list_items), len(list_values))
        for li in list_items:
            id = int(li.input.get('value'))
            name = li.text.strip()
            self.assertIn(id, list_values)
            self.assertEqual(name, list_values[id])
