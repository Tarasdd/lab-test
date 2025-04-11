from eshop.service import OrderService

def main():
    service = OrderService()

    order_id = "order456"
    order_data = {
        "customer": "Bob",
        "product": "Backpack",
        "status": "processing"
    }

    service.place_order(order_id, order_data)

if __name__ == "__main__":
    main()


