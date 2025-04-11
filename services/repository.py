from services.db import DynamoDBClient

class OrderRepository:
    def __init__(self):
        self.db = DynamoDBClient()

    def save_order(self, order_data: dict):
        self.db.create_table()
        self.db.put_order(order_data["order_id"], order_data)