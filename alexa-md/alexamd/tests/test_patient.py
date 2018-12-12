import unittest
import json
from test_base import AlexaMDTestBase
import os


class TestOpenPatient(AlexaMDTestBase):

    def test_default(self):
        response = self.app.post('/', data=self.openIntent('1'))
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.data)
        list_items = self.getListItemsFromResponse(response_data)
        session_attributes = self.getSessionAttributesFromResponse(response_data)

        self.assertListEqual(list_items, ['CT', 'MR'])
        self.assertDictEqual(session_attributes, {'patient': '1', 'level': 'patient'})

    def test_empty(self):
        self._execute_sql_command("insert into patients(p_first, p_last) values ('test', 'patient')")

        response = self.app.post('/', data=self.openIntent('5'))
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.data)
        list_items = self.getListItemsFromResponse(response_data)
        session_attributes = self.getSessionAttributesFromResponse(response_data)

        self.assertListEqual(list_items, [])
        self.assertDictEqual(session_attributes, {'patient': '5', 'level': 'patient'})

    def test_empty_study(self):
        self._execute_sql_command("insert into patients(p_first, p_last) values ('test', 'patient')")
        self._execute_sql_command("insert into collections(c_name, study, pid) values ('test', 'CT', 5)")

        response = self.app.post('/', data=self.openIntent('5'))
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.data)
        list_items = self.getListItemsFromResponse(response_data)
        session_attributes = self.getSessionAttributesFromResponse(response_data)

        self.assertListEqual(list_items, ['CT'])
        self.assertDictEqual(session_attributes, {'patient': '5', 'level': 'patient'})
