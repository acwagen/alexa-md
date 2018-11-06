from boto.s3.connection import S3Connection
import boto3
from alexamd_upload import model


def s3validate():
    """Compare contents of S3 bucket with database to detect inconsistencies."""
    s3 = boto3.client('s3')
    resp = s3.list_objects_v2(Bucket='alexa-md-495')

    db = model.get_db()

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

    file is a PNG.Image object. (This may need to be changed.)
    """

    print('Uploading {} to S3 as {}.'.format(file, id))


def s3delete(id):
    """Remove file with name id from our S3 bucket."""

    print('Removing {} from S3.'.format(id))



def s3fetch(id):
    """Get url for file with name id from our S3 bucket."""
    s3 = boto3.client('s3')

    filename = '{}.jpg'.format(id)

    s3.head_object(Bucket='alexa-md-495', Key=filename)
    url = s3.generate_presigned_url('get_object',Params={'Bucket':'alexa-md-495','Key':filename,})
    base_url = url.split('?')[0]

    return base_url
