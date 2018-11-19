import unittest
from alexamd_upload import app
import boto3
import filecmp
from test_base import TestAlexaMDUploadBase
# from mock import patch
from moto import mock_s3
from s3utils import s3upload, s3delete
import os
import io

@mock_s3()
class TestS3Delete(TestAlexaMDUploadBase):
    # docs.getmoto.org/en/latest/docs/getting_started.html

    def test_upload_to_s3(self):
        conn = boto3.resource('s3', region_name='us-east-2')
        # We need to create the bucket since this is all in Moto's 'virtual' AWS account
        test_bucket = 'test_bucket_1'
        conn.create_bucket(Bucket=test_bucket)
        mock_bucket = conn.Bucket(test_bucket)

        image_id = 'test0.png'
        image_id2 = 'test1.png'
        test_image = os.path.join(self.RESOURCES_DIR, image_id)
        test_image2 = os.path.join(self.RESOURCES_DIR, image_id2)

        s3_items = mock_bucket.objects.all()
        assert(len(s3_items) == 0)

        f1 = open(test_image, 'rb')
        f1 = io.BytesIO()
        with io.BytesIO() as image:
            test_image.save(image)
            image.seek(0)
            s3upload(image_id, image, s3_bucket=test_bucket)
        
        s3_items = mock_bucket.objects.all()
        assert(len(s3_items) == 1)

        mock_bucket.download_file(image_id, image_id2)

        assert(filecmp.cmp(test_image, test_image2))


    def test_delete_from_s3(self):
        conn = boto3.resource('s3', region_name='us-east-2')
        # We need to create the bucket since this is all in Moto's 'virtual' AWS account
        test_bucket = 'test_bucket_2'
        conn.create_bucket(Bucket='test_bucket_2')
        mock_bucket = conn.Bucket('test_bucket_2')

        image_id = 'test0.png'
        test_image = os.path.join(self.RESOURCES_DIR, image_id)

        s3_items = mock_bucket.objects.all()
        assert(len(s3_items) == 0)

        f1 = open(test_image, 'rb')
        f1 = io.BytesIO()
        with io.BytesIO() as image:
            test_image.save(image)
            image.seek(0)
            s3upload(image_id, image, s3_bucket=test_bucket)
        
        s3_items = mock_bucket.objects.all()
        assert(len(s3_items) == 1)

        # s3delete
        items_to_delete = [ image_id ]
        s3delete(items_to_delete, s3_bucket=test_bucket)

        s3_items = mock_bucket.objects.all()
        assert(len(s3_items) == 1)


    # https://stackoverflow.com/questions/36138250/how-do-i-test-methods-using-boto3-with-moto
    # def setUp(self):
    #     self.mock_s3.start()
    #     self.bucket_name = 'test_bucket_1'
    #     self.location = 'us-east-2'
    #     self.key_name = 'asdf'
    #     self.key_contents = 'asdf'
    #     s3 = boto.connect_s3()
    #     bucket = s3.create_bucket(self.bucket_name, location=self.location)
    #     # k = Key(bucket)
    
    # def tearDown(self):
    #     self.mock_s3.stop()
