import unittest
from alexamd_upload import app
import requests
import bs4
from test_base import TestAlexaMDUploadBase
from mock import patch
import os

class TestUpload(TestAlexaMDUploadBase):
    def upload(self, url, filepaths, collection, new_collection=None):
        # from https://stackoverflow.com/questions/47216204/how-do-i-upload-multiple-files-using-the-flask-test-client
        files = []
        try:
            files = [open(fpath, 'rb') for fpath in filepaths]
            data = {
                'files': files,
                'collection': collection
            }
            if new_collection:
                data['new_collection'] = new_collection
            return self.app.post(url, data=data)
        finally:
            for fp in files:
                fp.close()

    def test_default(self):
        option_values = { -1 : 'New Sequence',
                           1 : 'alyssa_CT',
                           2 : 'alyssa_MRI' }
        self.assertOptions('/patient/1/upload/', option_values)

    @patch('alexamd_upload.views.views.s3upload')
    def test_single_image(self, s3upload_function):
        response = self.upload('/patient/1/upload/',
                               [ os.path.join(self.RESOURCES_DIR, 'test1-CT.dcm')],
                               1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(s3upload_function.call_count, 1)
        # assert number of images in sequence

    @patch('alexamd_upload.views.views.s3upload')
    def test_multiple_images(self, s3upload_function):
        response = self.upload('/patient/1/upload/',
                               [ os.path.join(self.RESOURCES_DIR, 'test1-CT.dcm'),
                                 os.path.join(self.RESOURCES_DIR, 'test0-CT.dcm')],
                               1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(s3upload_function.call_count, 2)
        # assert number of images in sequence

    @patch('alexamd_upload.views.views.s3upload')
    def test_with_new_sequence(self, s3upload_function):
        response = self.upload('/patient/1/upload/',
                               [os.path.join(self.RESOURCES_DIR, 'test2-OT.dcm')],
                               -1,
                               new_collection='test sequence')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(s3upload_function.call_count, 1)

        option_values = { -1 : 'New Sequence',
                           1 : 'alyssa_CT',
                           2 : 'alyssa_MRI',
                           9 : 'test sequence' }
        self.assertOptions('/patient/1/upload/', option_values)
        # assert number of images in sequence

    @patch('alexamd_upload.views.views.s3upload')
    def test_invalid_image(self, s3upload_function):
        response = self.upload('/patient/1/upload/',
                               [os.path.join(self.RESOURCES_DIR, 'invalid.txt')],
                               1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(s3upload_function.call_count, 0)

    @patch('alexamd_upload.views.views.s3upload')
    def test_multiple_modalities(self, s3upload_function):
        response = self.upload('/patient/1/upload/',
                               [os.path.join(self.RESOURCES_DIR, 'test1-CT.dcm'),
                               os.path.join(self.RESOURCES_DIR, 'test2-OT.dcm')],
                               -1,
                               new_collection='test sequence')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(s3upload_function.call_count, 1)

        option_values = { -1 : 'New Sequence',
                           1 : 'alyssa_CT',
                           2 : 'alyssa_MRI',
                           9 : 'test sequence'}
        self.assertOptions('/patient/1/upload/', option_values)
        # assert number of images in sequence

    @patch('alexamd_upload.views.views.s3upload')
    def test_different_modality_existing_collection(self, s3upload_function):
        response = self.upload('/patient/1/upload/',
                               [ os.path.join(self.RESOURCES_DIR, 'test2-OT.dcm')],
                               1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(s3upload_function.call_count, 0)
        # assert number of images in sequence
