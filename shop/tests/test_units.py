from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Purchase
from decimal import Decimal

class ProductUnitTestCase(TestCase):
    def setUp(self):
        self.product_in_stock = Product.objects.create(
            name="Laptop", price=Decimal("1200.00"), stock=10)
        self.product_out_of_stock = Product.objects.create(
            name="Tablet", price=Decimal("600.00"), stock=0)

    def test_is_available(self):
        """Тестируем метод is_available"""
        self.assertTrue(self.product_in_stock.is_available(5))  # Товар доступен, если на складе достаточно.
        self.assertFalse(self.product_out_of_stock.is_available(1))  # Товар недоступен, если нет на складе.

    def test_decrease_stock(self):
        """Тестируем метод decrease_stock"""
        initial_stock = self.product_in_stock.stock
        self.product_in_stock.decrease_stock(1)  # Уменьшаем запас на 1
        self.product_in_stock.refresh_from_db()  # Обновляем объект из базы данных
        self.assertEqual(self.product_in_stock.stock, initial_stock - 1)  # Проверяем, что запас уменьшился.

    def test_decrease_stock_with_error(self):
        """Тестируем, что будет ошибка, если товаров недостаточно на складе"""
        with self.assertRaises(ValueError):
            self.product_out_of_stock.decrease_stock(1)  # Не можем уменьшить, если товара нет.