import pytest
from app.eshop import Product, ShoppingCart, Order
from services.repository import OrderRepository
from services.publisher import MessagePublisher
from services.service import OrderService
from unittest.mock import MagicMock


# Перевірка коректного створення продукту
def test_create_valid_product():
    p = Product("Laptop", 1200.0, 10)
    assert p.name == "Laptop"
    assert p.price == 1200.0
    assert p.available_amount == 10


# Перевірка, що продукт з некоректними даними не створюється
def test_create_invalid_product():
    with pytest.raises(ValueError):
        Product("", -50, -1)


# Перевірка методу is_available() для доступності товару
def test_is_product_available():
    p = Product("Mouse", 50.0, 5)
    assert p.is_available(3)
    assert not p.is_available(10)


# Перевірка додавання продукту в кошик
def test_add_product_to_cart():
    cart = ShoppingCart()
    p = Product("Keyboard", 100.0, 3)
    cart.add_product(p, 2)
    assert cart.contains_product(p)
    assert cart.calculate_total() == 200.0
    assert p.available_amount == 1  # зменшення кількості в наявності


# Перевірка додавання товару з некоректною кількістю
def test_add_invalid_amount_to_cart():
    cart = ShoppingCart()
    p = Product("Monitor", 200.0, 2)
    with pytest.raises(ValueError):
        cart.add_product(p, 0)


# Перевірка видалення продукту з кошика
def test_remove_product_from_cart():
    cart = ShoppingCart()
    p = Product("USB", 10.0, 5)
    cart.add_product(p, 2)
    cart.remove_product(p)
    assert not cart.contains_product(p)


# Перевірка, що не можна створити замовлення з порожнього кошика
def test_submit_empty_cart_order():
    cart = ShoppingCart()
    with pytest.raises(ValueError):
        cart.submit_cart_order()


# Перевірка створення і розміщення замовлення
def test_order_creation_and_placement():
    cart = ShoppingCart()
    p = Product("SSD", 150.0, 4)
    cart.add_product(p, 2)
    order = Order(cart)
    result = order.place_order()
    assert result["total_price"] == 300.0
    assert order.placed
    assert result["items"][0]["name"] == "SSD"


# Перевірка, що не можна оформити одне й те саме замовлення двічі
def test_place_order_twice():
    cart = ShoppingCart()
    p = Product("GPU", 500.0, 2)
    cart.add_product(p, 1)
    order = Order(cart)
    order.place_order()
    with pytest.raises(ValueError):
        order.place_order()


# Перевірка повного сценарію роботи OrderService з моками
def test_order_service_flow():
    mock_repo = MagicMock(spec=OrderRepository)
    mock_publisher = MagicMock(spec=MessagePublisher)
    service = OrderService(mock_repo, mock_publisher)

    cart = service.create_cart()
    product = Product("Router", 80.0, 10)
    service.add_product_to_cart(cart, product, 3)
    order_data = service.place_order(cart)

    assert order_data["total_price"] == 240.0
    mock_repo.save_order.assert_called_once()  # перевірка збереження замовлення
    mock_publisher.publish_order_placed.assert_called_once_with(order_data)  # перевірка відправки повідомлення
