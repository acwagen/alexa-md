import unittest
import json
from test_base import AlexaMDTestBase
import os
import flask

class TestOpenStudy(AlexaMDTestBase):
    def test_default(self):
        # open study
        response = self.app.post('/', data=self.openIntent('1', session_attributes={'level': 'patient', 'patient': '1'}))
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.data)
        list_items = self.getListItemsFromResponse(response_data)
        session_attributes = self.getSessionAttributesFromResponse(response_data)

        self.assertListEqual(list_items, ['alyssa_CT'])
        self.assertDictEqual(session_attributes, {'patient': '1', 'study': 'CT', 'level': 'study'})
