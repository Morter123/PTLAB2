from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Purchase


class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="Книга", price=740, stock=1)

    def test_purchase_success_when_stock_available(self):
        response = self.client.post(reverse('buy', args=[self.product.id]), {
            'person': 'Покупатель',
            'address': 'Светлый путь, 10'
        })
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 1)
        self.assertEqual(response.status_code, 200)


    # def test_purchase_fails_when_no_stock_available(self):
    #     self.product.stock = 0
    #     self.product.save()
    #     response = self.client.post(reverse('buy', args=[self.product.id]), {
    #         'person': 'Петров',
    #         'address': 'ул. Темная'
    #     })
    #     self.assertEqual(response.status_code, 400)
    #     self.assertContains(
    #         response, 'Товар недоступен для покупки, недостаточно на складе.')
