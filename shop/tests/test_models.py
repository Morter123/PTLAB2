from django.test import TestCase
from shop.models import Product, Purchase
from decimal import Decimal
from datetime import datetime


class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="book", price=Decimal("740.00"), stock=10)
        Product.objects.create(name="pencil", price=Decimal("50.00"), stock=10)

    def test_correctness_types(self):
        """Проверка типов данных в модели Product."""
        self.assertIsInstance(Product.objects.get(name="book").name, str)
        self.assertIsInstance(Product.objects.get(name="book").price, Decimal)
        self.assertIsInstance(Product.objects.get(name="pencil").name, str)
        self.assertIsInstance(Product.objects.get(
            name="pencil").price, Decimal)

    def test_correctness_data(self):
        """Проверка корректности данных в модели Product."""
        self.assertEqual(Product.objects.get(
            name="book").price, Decimal("740.00"))
        self.assertEqual(Product.objects.get(
            name="pencil").price, Decimal("50.00"))


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.product_book = Product.objects.create(
            name="book", price=Decimal("740.00"), stock=5)
        self.datetime = datetime.now()
        Purchase.objects.create(product=self.product_book,
                                person="Ivanov", address="Svetlaya St.")

    def test_correctness_types(self):
        """Проверка типов данных в модели Purchase."""
        self.assertIsInstance(Purchase.objects.get(
            product=self.product_book).person, str)
        self.assertIsInstance(Purchase.objects.get(
            product=self.product_book).address, str)
        self.assertIsInstance(Purchase.objects.get(
            product=self.product_book).date, datetime)

    def test_correctness_data(self):
        """Проверка корректности данных в модели Purchase."""
        purchase = Purchase.objects.get(product=self.product_book)
        self.assertEqual(purchase.person, "Ivanov")
        self.assertEqual(purchase.address, "Svetlaya St.")
        self.assertEqual(purchase.date.replace(microsecond=0),
                         self.datetime.replace(microsecond=0))


class ProductStockTestCase(TestCase):
    def setUp(self):
        self.product_with_stock = Product.objects.create(
            name="Table", price=Decimal("2000.00"), stock=5)
        self.product_no_stock = Product.objects.create(
            name="Chair", price=Decimal("1000.00"), stock=0)

def test_stock_decreases_after_purchase(self):
    """Проверка уменьшения количества товара на складе после покупки."""
    initial_stock = self.product_with_stock.stock
    Purchase.objects.create(product=self.product_with_stock, person="Buyer", address="Test Street")
    self.product_with_stock.refresh_from_db()  # Обновляем объект из базы данных
    self.assertEqual(self.product_with_stock.stock, initial_stock - 1)  # Проверяем уменьшение количества



def test_purchase_fails_if_no_stock(self):
    """Проверка, что покупка не может быть завершена, если товара нет в наличии."""
    response = self.client.post(reverse('buy', args=[self.product_no_stock.id]), {
        'person': 'Buyer',
        'address': 'Test Street'
    })
    self.assertEqual(response.status_code, 400)  # Ожидаем ошибку
    self.assertContains(
        response, 'Товар недоступен для покупки, недостаточно на складе.')
