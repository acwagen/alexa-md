from boto.s3.connection import S3Connection
import boto3
import alexamd_upload
# from io import BytesIO
# from PIL import Image
import numpngw
import os


S3_BUCKET = alexamd_upload.app.config['S3_BUCKET']

def s3validate():
    """Compare contents of S3 bucket with database to detect inconsistencies."""
    s3 = boto3.client('s3')
    resp = s3.list_objects_v2(Bucket=S3_BUCKET)

    db = alexamd_upload.model.get_db()

    count = db.execute('select count(*) as count from images').fetchone()['count']
    if len(resp['Contents']) != count:
        print('S3 bucket size ({}) != database images ({})'.format(
            len(resp['Contents']), count))
        return False

    for img in resp['Contents']:
        filename = img['Key']
        image_id = filename.split('.')[0]

        # might be faster to load all images from database and then do lookups
        # instead of separate queries (just not memory efficient) ?
        exists = db.execute('select count(*) as count from images where iid = ?',
            (image_id,)).fetchone()['count']
        if exists == 0:
            print('Image {} doesn\'t exist in database'.format(image_id))
            return False

    return True


def s3upload(id, file):
    """Upload a file to our S3 bucket with name id.

    file is a readable BytesIO object.)
    """

    filename = '{}.png'.format(id)

    s3 = boto3.resource('s3')
    extra_s3_args = {
        "ContentType": "image/png",
        "ACL": "public-read"
    }

    s3.Bucket(S3_BUCKET).upload_fileobj(file, filename, ExtraArgs=extra_s3_args)


def s3delete(ids):
    """Remove files with names in ids list from our S3 bucket."""

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET)

    images_to_delete = []
    for id in ids:
        print('Removing {} from S3.'.format(id))
        images_to_delete.append({
            'Key': '{}.png'.format(id)
        })

    response = bucket.delete_objects(
        Delete={
            'Objects': images_to_delete
        },
    )
    print('Response: {}'.format(response))


def s3fetch(id):
    """Get url for file with name id from our S3 bucket."""
    s3 = boto3.client('s3')

    filename = '{}.png'.format(id)

    s3.head_object(Bucket=S3_BUCKET, Key=filename)
    url = s3.generate_presigned_url('get_object',Params={'Bucket':S3_BUCKET,'Key':filename,})
    base_url = url.split('?')[0]

    return base_url
