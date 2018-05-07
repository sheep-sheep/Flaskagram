# -*- encoding: UTF-8 -*-
import boto3
import os
from werkzeug.datastructures import FileStorage

from flaskagram import app

bucket_name = app.config['AWS_BUCKET_NAME']
save_dir = app.config['DOMAIN_PREFIX']
# domain_prefix = app.config['DOMAIN_PREFIX']

def s3_upload_file(source_file, save_file_name):
    s3 = boto3.resource('s3')
    if isinstance(source_file, FileStorage):
        data = source_file.read()
    elif isinstance(source_file, str):
        data = open(source_file, 'rb')
    else:
        data = source_file
    try:
        obj = s3.Bucket(bucket_name)
        obj.put_object(Key=save_file_name, Body=data)
        return '/image/' + os.path.join(save_dir, save_file_name)
    except Exception as e:
        print(e)
        return None
