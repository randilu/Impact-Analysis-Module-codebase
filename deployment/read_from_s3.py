import boto3
import json

from botocore.handlers import disable_signing
from src.data.fetch_trend_data_utils import write_json_data_to_file

def download_object_from_s3(s3_bucket_name, object_name, destination_to_save):
    try:
        s3 = boto3.resource('s3')
        #
        # for public buckets
        #
        s3.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
        #
        # authentication for bucket if required
        #

        # s3 = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY)

        content_object = s3.Object(s3_bucket_name, object_name)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        print(json_content)

        write_json_data_to_file(destination_to_save, json_content)

    except BaseException as e:
        print('Download error')
        print(str(e))


def download_csv_object_from_s3(s3_bucket_name, object_name, destination_to_save):
    try:
        s3 = boto3.resource('s3')
        #
        # for public buckets
        #
        s3.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
        #
        # authentication for bucket if required
        #

        # s3 = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY)

        content_object = s3.Object(s3_bucket_name, object_name)
        content_object.download_file(destination_to_save)

    except BaseException as e:
        print('Download error')
        print(str(e))
