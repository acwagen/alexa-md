import unittest
from alexamd_upload import app
# import requests
# import bs4
import boto
import boto3
import filecmp
from test_base import TestAlexaMDUploadBase
# from mock import patch
from moto import mock_s3
from s3utils import s3upload, s3delete
import os
import io

class TestS3Delete(TestAlexaMDUploadBase):
    mock_s3 = mock_s3()

    # docs.getmoto.org/en/latest/docs/getting_started.html

    @mock_s3()
    def test_s3_stuff():
        # stuff
        s3 = boto3.resource('s3')


    @mock_s3
    def test_upload_to_s3(self):
        conn = boto3.resource('s3', region_name='us-east-2')
        # We need to create the bucket since this is all in Moto's 'virtual' AWS account
        test_bucket = 'test_bucket_1'
        conn.create_bucket(Bucket=test_bucket)
        mock_bucket = conn.Bucket(test_bucket)

        test_image = os.path.join(self.RESOURCES_DIR, 'test0.png')
        test_filename = 'testfile.txt'
        test_filename2 = 'testfile2.txt'

        image_id = 'todochangethistexttosomethingmoresuitableimgoingtotkdnow.png'

        f1 = open(test_image, 'rb')
        f1 = io.BytesIO()
        with io.BytesIO() as image:
            test_image.save(image)
            image.seek(0)
            # image is now true file i want to upload or call
            s3upload(image_id, image)

        file = open(test_filename, 'w')
        file.write('Hello Dr. Chesney')
        file.close()

        # call function TODO DO THIS AND GET SOME IMAGE SOMEHOW
        # s3upload(filename, file, s3_bucket=test_bucket)

        s3_args = {"ACL": "public-read"}
        mock_bucket.upload_file(test_filename, test_filename, ExtraArgs=s3_args)
        # s3.Bucket(S3_BUCKET).upload_file(filename, filename, ExtraArgs=extra_s3_args)

        response = mock_bucket.download_file(test_filename, test_filename2)
        print('MY RESPONSE IS ||||| {} |||||'.format(response))
        if filecmp.cmp(test_filename, test_filename2):
            print('True')
        else:
            print('False')

        # TODO delete both files and bucket and do something with bool 38

        # body = conn.Object('mybucket', 'steve').get()['Body'].read().decode("utf-8")

        # assert body == b'is awesome
    
    @mock_s3
    def test_delete_from_s3():
        conn = boto3.resource('s3', region_name='us-east-2')
        # We need to create the bucket since this is all in Moto's 'virtual' AWS account
        conn.create_bucket(Bucket='test_bucket_2')
        mock_bucket = conn.Bucket('test_bucket_2')

        test_filename = 'testfile.txt'
        file = open(test_filename, 'w')
        file.write('Hello Dr. Chesney')
        file.close()

        s3_args = {"ACL": "public-read"}
        mock_bucket.upload_file(test_filename, test_filename, ExtraArgs=s3_args)
        
        s3delete

        s3_items = mock_bucket.objects.all()

        assert(len(s3_items) == 1)


    # https://stackoverflow.com/questions/36138250/how-do-i-test-methods-using-boto3-with-moto
    def setUp(self):
        self.mock_s3.start()
        self.bucket_name = 'test_bucket_1'
        self.location = 'us-east-2'
        self.key_name = 'asdf'
        self.key_contents = 'asdf'
        s3 = boto.connect_s3()
        bucket = s3.create_bucket(self.bucket_name, location=self.location)
        # k = Key(bucket)
    
    def tearDown(self):
        self.mock_s3.stop()
    
    def test_s3_boto3(self):
        s3 = boto3.resource('s3', region_name=self.location)
        bucket = s3.Bucket(self.bucket_name)
        assert bucket.name == self.bucket_name
        # retrieve already setup keys
        keys = list(bucket.objects.filter(Prefix=self.key_name))
        assert len(keys) == 1
        assert keys[0].key == self.key_name
        # update key
        s3.Object(self.bucket_name, self.key_name).put(Body='new')
