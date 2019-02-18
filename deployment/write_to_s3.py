import boto3

from botocore.handlers import disable_signing
from src.data.fetch_trend_data_utils import read_json_data_from_file

ACCESS_ID = ' AKIAIR6DQWSOVXCJAXPA'
ACCESS_KEY = 't5EMmjUapCKo/Ta2S1QUmCQWEsY3HOQwXCqL7+Hy'

s3_bucket_name = 'fypiamawsbucket'
object_name = 'kelani_valley_impact_events.json'
file = '/home/randilu/fyp_integration/Impact-Analysis-Module/data/processed/final_output/' + object_name

try:
    impact_events = read_json_data_from_file(file)

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
    s3.Object(s3_bucket_name, object_name).put(Body=impact_events)
    print('File Successfully Uploaded!')


except BaseException as e:
    print('Uploaded error!')
    print(str(e))
