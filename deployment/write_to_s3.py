import boto3
from src.constants.constants import *

from botocore.handlers import disable_signing
from src.data.fetch_trend_data_utils import read_json_data_from_file

ACCESS_ID = USER1_ACCESS_ID
ACCESS_KEY = USER1_ACCESS_KEY


# s3_bucket_name = 'fypiamawsbucket'
# object_name = 'kelani_valley_impact_events.json'
# source_file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/final_output/' + object_name

def upload_output_to_s3(s3_bucket_name, object_name, source_file):
    try:
        impact_events = read_json_data_from_file(source_file)

        s3 = boto3.resource('s3')
        #
        # disable signing for public buckets
        #
        s3.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
        #
        # authentication for bucket if required
        #

        s3 = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY)

        content_object = s3.Object(s3_bucket_name, object_name)
        content_object.put(Body=impact_events)
        print('File Successfully Uploaded!')

    except BaseException as e:
        print('Uploaded error!')
        print(str(e))
