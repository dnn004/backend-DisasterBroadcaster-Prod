import boto3
from django.conf import settings

def s3_delete(id):
  s3 = boto3.resource('s3')
  s3.Object(settings.AWS_STORAGE_BUCKET_NAME, str(id)).delete()