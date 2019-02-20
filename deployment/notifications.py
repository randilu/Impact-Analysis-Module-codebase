import boto3

AWS_ACCESS_KEY = 'AKIAIR6DQWSOVXCJAXPA'
AWS_SECRET_ACCESS_KEY = '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'

SQS_QUEUE_NAME = 'fyp_company_dataq'

sqs_resource_connection = boto3.resource(
    'sqs',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='ap-southeast-1'
)

queue = sqs_resource_connection.Queue('https://sqs.ap-southeast-1.amazonaws.com/190366723864/fyp_company_dataq')

# queue = sqs_resource_connection.get_queue_by_name(QueueName=SQS_QUEUE_NAME)

messages = queue.receive_messages(MaxNumberOfMessages=5, WaitTimeSeconds=10)
for message in messages:
    print(message.body)
    message.delete()  # delete the message from the queue

response = queue.send_message(MessageBody='Hello by AWS SDK for Python!')
