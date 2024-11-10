from django.test import TestCase
from shop.models import Product, Purchase
from datetime import datetime
from decimal import Decimal


class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="book", price=Decimal("740.00"), stock=10)
        Product.objects.create(name="pencil", price=Decimal("50.00"), stock=10)

    def test_correctness_types(self):
        self.assertIsInstance(Product.objects.get(name="book").name, str)
        self.assertIsInstance(Product.objects.get(name="book").price, Decimal)
        self.assertIsInstance(Product.objects.get(name="pencil").name, str)
        self.assertIsInstance(Product.objects.get(name="pencil").price, Decimal)

    def test_correctness_data(self):
        self.assertTrue(Product.objects.get(name="book").price == Decimal("740.00"))
        self.assertTrue(Product.objects.get(name="pencil").price == Decimal("50.00"))


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.product_book = Product.objects.create(name="book", price=Decimal("740.00"), stock=5)
        self.datetime = datetime.now()
        Purchase.objects.create(product=self.product_book, person="Ivanov", address="Svetlaya St.")

    def test_correctness_types(self):
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).person, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).address, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).date, datetime)

    def test_correctness_data(self):
        self.assertTrue(Purchase.objects.get(product=self.product_book).person == "Ivanov")
        self.assertTrue(Purchase.objects.get(product=self.product_book).address == "Svetlaya St.")
        self.assertTrue(Purchase.objects.get(product=self.product_book).date.replace(microsecond=0) ==
                        self.datetime.replace(microsecond=0))


class ProductStockTestCase(TestCase):
    def setUp(self):
        self.product_with_stock = Product.objects.create(name="Стол", price=Decimal("2000.00"), stock=5)
        self.product_no_stock = Product.objects.create(name="Стул", price=Decimal("1000.00"), stock=0)

    def test_stock_decreases_after_purchase(self):
        initial_stock = self.product_with_stock.stock
        Purchase.objects.create(product=self.product_with_stock, person="Покупатель", address="улица Тестовая")
        self.product_with_stock.refresh_from_db()
        self.assertEqual(self.product_with_stock.stock, initial_stock - 1)

    def test_purchase_fails_if_no_stock(self):
        with self.assertRaises(ValueError):
            Purchase.objects.create(product=self.product_no_stock, person="Покупатель", address="улица Тестовая")
