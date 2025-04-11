import os

class Config:
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL", "http://localhost:4566")
    SQS_ENDPOINT_URL = os.getenv("SQS_ENDPOINT_URL", "http://localhost:4566")
    DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "ShippingOrders")
    SQS_QUEUE_NAME = os.getenv("SQS_QUEUE_NAME", "ShippingQueue")