import unittest
from alexamd_upload import app
import requests
import bs4
from test_base import TestAlexaMDUploadBase
from mock import patch
import os

class TestUpload(TestAlexaMDUploadBase):
    def upload(self, url, filepaths, collection):
        # from https://stackoverflow.com/questions/47216204/how-do-i-upload-multiple-files-using-the-flask-test-client
        files = []
        try:
            files = [open(fpath, 'rb') for fpath in filepaths]
            return self.app.post(url, data={
                'files': files,
                'collection': collection
            })
        finally:
            for fp in files:
                fp.close()

    def test_default(self):
        option_values = { -1 : 'New Sequence',
                           1 : 'alyssa_CT',
                           2 : 'alyssa_MRI' }
        self.assertOptions('/patient/1/upload/', option_values)

    @unittest.skip('Not Implemented Yet')
    @patch('alexamd_upload.views.views.s3upload')
    def test_single_image(self, s3upload_function):
        pass

    @unittest.skip('Not Implemented Yet')
    @patch('alexamd_upload.views.views.s3upload')
    def test_multiple_images(self, s3upload_function):
        pass

    @unittest.skip('Not Implemented Yet')
    @patch('alexamd_upload.views.views.s3upload')
    def test_with_new_sequence(self, s3upload_function):
        pass

    @unittest.skip('Not Implemented Yet')
    @patch('alexamd_upload.views.views.s3upload')
    def test_with_existing_sequence(self, s3upload_function):
        pass

    @patch('alexamd_upload.views.views.s3upload')
    def test_invalid_image(self, s3upload_function):
        response = self.upload('/patient/1/upload/',
                               [os.path.join(self.RESOURCES_DIR, 'invalid.txt')],
                               1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(s3upload_function.call_count, 0)


    @unittest.skip('Not Implemented Yet')
    @patch('alexamd_upload.views.views.s3upload')
    def test_multiple_modalities(self, s3upload_function):
        pass
