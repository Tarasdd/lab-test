import boto3
from botocore.exceptions import ClientError
from services.config import Config

class MessagePublisher:
    def __init__(self):
        self.sqs = boto3.client(
            'sqs',
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test',
            endpoint_url='http://localhost:4566'  # якщо використовуєш localstack або аналог
        )
        self.queue_name = Config.SQS_QUEUE_NAME
        self.queue_url = self._get_or_create_queue()

    def _get_or_create_queue(self):
        try:
            response = self.sqs.get_queue_url(QueueName=self.queue_name)
            print(f"Queue {self.queue_name} already exists.")
            return response['QueueUrl']
        except ClientError:
            print(f"Creating queue {self.queue_name}...")
            response = self.sqs.create_queue(QueueName=self.queue_name)
            return response['QueueUrl']

    def publish_order_placed(self, message_body: dict):
        import json
        response = self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(message_body)
        )
        print(f"Message sent. ID: {response['MessageId']}")
