from typing import Dict
import uuid

class Product:
    def __init__(self, name: str, price: float, available_amount: int):
        if not name or not isinstance(name, str):
            raise ValueError("Invalid product name")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Invalid product price")
        if not isinstance(available_amount, int) or available_amount < 0:
            raise ValueError("Invalid product availability")

        self.name = name
        self.price = price
        self.available_amount = available_amount

    def is_available(self, requested_amount: int) -> bool:
        return isinstance(requested_amount, int) and requested_amount > 0 and self.available_amount >= requested_amount

    def buy(self, requested_amount: int):
        if not self.is_available(requested_amount):
            raise ValueError("Not enough products available")

class ShoppingCart:
    def __init__(self):
        self.products: Dict[Product, int] = {}

    def contains_product(self, product: Product) -> bool:
        return product in self.products

    def calculate_total(self) -> float:
        return sum(p.price * count for p, count in self.products.items())

    def add_product(self, product: Product, amount: int):
        if not isinstance(product, Product):
            raise TypeError("Invalid product type")
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Invalid amount")
        if not product.is_available(amount):
            raise ValueError(f"Product {product.name} has only {product.available_amount} items")
        self.products[product] = self.products.get(product, 0) + amount
        product.available_amount -= amount

    def remove_product(self, product: Product):
        if product in self.products:
            del self.products[product]

    def submit_cart_order(self):
        if not self.products:
            raise ValueError("Cannot place an order with an empty cart")
        self.products.clear()

class Order:
    def __init__(self, cart: ShoppingCart):
        if not isinstance(cart, ShoppingCart):
            raise TypeError("Invalid cart instance")
        if not cart.products:
            raise ValueError("Cannot create an order with an empty cart")

        self.cart = cart
        self.placed = False
        self.order_id = str(uuid.uuid4())

    def place_order(self) -> Dict:
        if self.placed:
            raise ValueError("Order has already been placed")

        total_price = self.cart.calculate_total()
        order_items = [
            {"name": p.name, "price": p.price, "amount": amount}
            for p, amount in self.cart.products.items()
        ]

        self.cart.submit_cart_order()
        self.placed = True

        return {
            "order_id": self.order_id,
            "items": order_items,
            "total_price": total_price
        }