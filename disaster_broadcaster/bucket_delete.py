import boto3
import os
from django.conf import settings

def s3_delete(id):
  s3 = boto3.resource('s3')
  s3.Object(os.environ.get('S3_BUCKET_NAME'), str(id)).delete()