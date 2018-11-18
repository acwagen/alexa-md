import unittest
from alexamd_upload import app
import requests
import bs4
from test_base import TestAlexaMDUploadBase
from mock import patch

class TestS3Upload(TestAlexaMDUploadBase):
    def test_default(self):
        option_values = { 1 : 'w, alyssa',
                    2 : 's, anthony',
                    3 : 'y, derek',
                    4 : 'w, mike' }
        self.assertOptions('/', option_values)

    def test_index_after_select(self):
        response = self.app.post('/', data=dict(patient=2))
        self.assertEqual(response.status_code, 200)

        option_values = { 1 : 'w, alyssa',
                    2 : 's, anthony',
                    3 : 'y, derek',
                    4 : 'w, mike' }
        self.assertOptions('/', option_values, selected=2)

    @patch('alexamd_upload.views.views.s3delete')
    def test_index_with_select_after_delete(self, s3delete_function):
        response = self.app.post('/manage/', data=dict(id=2))
        self.assertEqual(response.status_code, 200)

        option_values = { 1 : 'w, alyssa',
                    3 : 'y, derek',
                    4 : 'w, mike' }
        self.assertOptions('/', option_values)


    def test_index_after_create(self):
        response = self.app.post('/manage/', data=dict(name='test patient'))
        self.assertEqual(response.status_code, 200)

        option_values = { 1 : 'w, alyssa',
                    2 : 's, anthony',
                    3 : 'y, derek',
                    4 : 'w, mike',
                    5 : 'patient, test' }
        self.assertOptions('/', option_values)
