from boto.s3.connection import S3Connection
import boto3

def s3upload(file):
    print('Uploading {}'.format(file))


"""
s3fetch(file_name):
    s3 = boto3.client('s3')

    file_name = filename + ".jpg"
    file_name = file_name.lower()

   s3.head_object(Bucket='alexa-md-495', Key=file_name)
   url = s3.generate_presigned_url('get_object',Params={'Bucket':'alexa-md-495','Key':file_name,})
   parts = url.split('?')
   true_url = parts[0]

s3iterate():
    s3 = boto3.client('s3')
    resp = s3.list_objects_v2(Bucket='alexa-md-495')

    for obj in resp['Contents']:
        file_name = obj['Key']
        true_file_name = file_name.split('.')[0]
        url = s3.generate_presigned_url('get_object',Params={'Bucket':'alexa-md-495','Key':file_name,})
        parts = url.split('?')
        true_url = parts[0]
"""
