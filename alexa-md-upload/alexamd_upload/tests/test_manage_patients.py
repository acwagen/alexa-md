import unittest
from alexamd_upload import app
import requests
import bs4
from test_base import TestAlexaMDUploadBase
from mock import patch

class TestManagePatients(TestAlexaMDUploadBase):
    def test_default(self):
        list_values = { 1 : 'w, alyssa',
                        2 : 's, anthony',
                        3 : 'y, derek',
                        4 : 'w, mike' }
        self.assertListItems('/manage/', list_values)

    @patch('alexamd_upload.views.views.s3delete')
    def test_delete_patient(self, s3delete_function):
        response = self.app.post('/manage/', data=dict(id=1))
        self.assertEqual(response.status_code, 200)

        s3delete_call_args = ['alyssa1', 'alyssa2', 'alyssa3', 'alyssa4']
        self.assertEqual(s3delete_function.call_count, 1)
        self.assertItemsEqual(s3delete_function.call_args_list[0][0][0], s3delete_call_args)

        list_values = { 2 : 's, anthony',
                        3 : 'y, derek',
                        4 : 'w, mike' }
        self.assertListItems('/manage/', list_values)

    def test_create_patient(self):
        response = self.app.post('/manage/', data=dict(name='test patient'))
        self.assertEqual(response.status_code, 200)

        list_values = { 1 : 'w, alyssa',
                        2 : 's, anthony',
                        3 : 'y, derek',
                        4 : 'w, mike',
                        5 : 'patient, test' }
        self.assertListItems('/manage/', list_values)
