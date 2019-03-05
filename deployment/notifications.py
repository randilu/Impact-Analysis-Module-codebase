import boto3
import time
from deployment.falsk_app.process import trigger_main_process
from src.constants.constants import *

ACCESS_ID = USER1_ACCESS_ID
ACCESS_KEY = USER1_ACCESS_KEY


def alert_for_sqs_notifications():
    sqs_resource_connection = boto3.resource(
        'sqs',
        aws_access_key_id=ACCESS_ID,
        aws_secret_access_key=ACCESS_KEY,
        region_name='ap-southeast-1'
    )

    queue = sqs_resource_connection.Queue('https://sqs.ap-southeast-1.amazonaws.com/190366723864/fyp_company_dataq')

    # queue = sqs_resource_connection.get_queue_by_name(QueueName=SQS_QUEUE_NAME)
    while True:
        messages = queue.receive_messages(MaxNumberOfMessages=1, WaitTimeSeconds=2)
        print('...........')
        if messages:
            for message in messages:
                print(message.body)
                message.delete()  # delete the message from the queue
                trigger_main_process()
            return True
        else:
            print('no msgs')
            time.sleep(2)
