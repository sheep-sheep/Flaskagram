# -*- encoding: UTF-8 -*-
import boto3
from flaskagram import app


def s3_upload_file(source_file, save_file_name):
    s3 = boto3.resource('s3')
    data = open(source_file, 'rb')
    obj = s3.Bucket(app.config['AWS_BUCKET_NAME'])
    response = obj.put_object(Key=save_file_name, Body=data)
    return None
