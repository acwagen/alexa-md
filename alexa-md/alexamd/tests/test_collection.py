import unittest
import json
from test_base import AlexaMDTestBase
import os
import flask

class TestOpenCollection(AlexaMDTestBase):
    def test_default(self):
        response = self.app.post('/', data=self.openIntent('1', session_attributes={'level': 'study', 'patient': '1', 'study': 'CT'}))
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.data)
        session_attributes = self.getSessionAttributesFromResponse(response_data)

        self.assertDictEqual(session_attributes, {'patient': '1', 'study': 'CT', 'level': 'image', 'collection': '1', 'index': 0})
