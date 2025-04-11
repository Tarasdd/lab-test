from app.eshop import ShoppingCart, Product, Order
from services.repository import OrderRepository
from services.publisher import MessagePublisher

class OrderService:
    def __init__(self, repository: OrderRepository, publisher: MessagePublisher):
        self.repository = repository
        self.publisher = publisher

    def create_cart(self) -> ShoppingCart:
        return ShoppingCart()

    def add_product_to_cart(self, cart: ShoppingCart, product: Product, amount: int):
        cart.add_product(product, amount)

    def place_order(self, cart: ShoppingCart):
        order = Order(cart)
        order_data = order.place_order()
        self.repository.save_order(order_data)
        self.publisher.publish_order_placed(order_data)
        return order_data