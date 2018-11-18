from boto.s3.connection import S3Connection
import boto3
import alexamd_upload
# from io import BytesIO
# from PIL import Image
import numpngw
import os


# S3_BUCKET = alexamd_upload.app.config['S3_BUCKET']

def s3validate(s3_bucket=alexamd_upload.app.config['S3_BUCKET']):
    """Compare contents of S3 bucket with database to detect inconsistencies."""
    s3 = boto3.client('s3')
    resp = s3.list_objects_v2(Bucket=s3_bucket)

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


def s3upload(filename, file, s3_bucket=alexamd_upload.app.config['S3_BUCKET']):
    """Upload a file to our S3 bucket with name id.

    file is a readable BytesIO object.)
    """

    s3 = boto3.resource('s3')
    extra_s3_args = {
        "ContentType": "image/png",
        "ACL": "public-read"
    }

    s3.Bucket(s3_bucket).upload_fileobj(file, filename, ExtraArgs=extra_s3_args)


def s3delete(ids, s3_bucket=alexamd_upload.app.config['S3_BUCKET']):
    """Remove files with names in ids list from our S3 bucket."""

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_bucket)

    images_to_delete = []
    for id in ids:
        print('Removing {} from S3.'.format(id))
        images_to_delete.append({
            'Key': id
        })

    response = bucket.delete_objects(
        Delete={
            'Objects': images_to_delete
        },
    )
    print('Response: {}'.format(response))


def s3fetch(id, s3_bucket=alexamd_upload.app.config['S3_BUCKET']):
    """Get url for file with name id from our S3 bucket."""
    s3 = boto3.client('s3')

    filename = '{}.png'.format(id)

    s3.head_object(Bucket=s3_bucket, Key=filename)
    url = s3.generate_presigned_url('get_object',Params={'Bucket':S3_BUCKET,'Key':filename,})
    base_url = url.split('?')[0]

    return base_url
