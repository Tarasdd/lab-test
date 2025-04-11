from app.eshop import Product
from services.service import OrderService
from services.repository import OrderRepository
from services.publisher import MessagePublisher

repository = OrderRepository()
publisher = MessagePublisher()
order_service = OrderService(repository, publisher)

apple = Product("Apple", 1.5, 10)
banana = Product("Banana", 2.0, 5)

cart = order_service.create_cart()

try:
    order_service.add_product_to_cart(cart, apple, 3)
    order_service.add_product_to_cart(cart, banana, 2)
except ValueError as e:
    print(f"[ERROR] {e}")

try:
    order_data = order_service.place_order(cart)
    print("[SUCCESS] Order placed successfully!")
    print("Order details:", order_data)
except ValueError as e:
    print(f"[ERROR] {e}")