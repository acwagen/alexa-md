import unittest
from alexamd_upload import app
import requests
import bs4
from test_base import TestAlexaMDUploadBase
from mock import patch

class TestManageCollections(TestAlexaMDUploadBase):
    def test_default(self):
        list_values = { 1 : 'alyssa_CT (3 images)',
                        2 : 'alyssa_MRI (1 image)' }
        self.assertListItems('/patient/1/manage/', list_values)

    @patch('alexamd_upload.views.views.s3delete')
    def test_delete_collection(self, s3delete_function):
        response = self.app.post('/patient/1/manage/', data=dict(id=1))
        self.assertEqual(response.status_code, 200)

        s3delete_call_args = ['alyssa1', 'alyssa3', 'alyssa4']
        self.assertEqual(s3delete_function.call_count, 1)
        self.assertItemsEqual(s3delete_function.call_args_list[0][0][0], s3delete_call_args)

        list_values = { 2 : 'alyssa_MRI (1 image)' }
        self.assertListItems('/patient/1/manage/', list_values)
