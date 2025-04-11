import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
from services.config import Config


def convert_floats_to_decimals(obj):
    if isinstance(obj, list):
        return [convert_floats_to_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_floats_to_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, float):
        return Decimal(str(obj))  # уникнення втрати точності
    else:
        return obj


class DynamoDBClient:
    def __init__(self):
        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=Config.AWS_REGION,
            endpoint_url=Config.DYNAMODB_ENDPOINT_URL,
            aws_access_key_id="fakeMyKeyId",
            aws_secret_access_key="fakeSecretAccessKey"
        )
        self.table_name = Config.DYNAMODB_TABLE_NAME

    def create_table(self):
        try:
            table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[{"AttributeName": "order_id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "order_id", "AttributeType": "S"}],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )
            table.wait_until_exists()
            print(f"Table {self.table_name} created.")
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceInUseException':
                raise
            print(f"Table {self.table_name} already exists.")

    def put_order(self, order_id: str, item: dict):
        item_converted = convert_floats_to_decimals(item)
        table = self.dynamodb.Table(self.table_name)
        table.put_item(Item={"order_id": order_id, **item_converted})
        print(f"Order {order_id} saved.")
