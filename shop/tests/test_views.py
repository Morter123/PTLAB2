from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from shop.models import Product, Purchase
from shop.views import PurchaseCreate


class ShopViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Luxury Watch',
            price=1000,
            stock=10
        )


    def test_index_view(self):
        Product.objects.create(name='Product 1', price=100, stock=5)
        Product.objects.create(name='Product 2', price=200, stock=3)

        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Product 2')

    def test_purchase_create_view_success(self):
        
        self.product.stock = 10
        self.product.save()

        response = self.client.post(
            reverse('buy', args=[self.product.id]),
            {'product': self.product.id, 'person': 'Тестовый Покупатель',
                'address': 'Тестовый Адрес'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Спасибо за покупку, Тестовый Покупатель!")
        

    def test_purchase_create_view_no_product(self):
        # Попытка покупки несуществующего товара
        response = self.client.post(reverse('buy', args=[999]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

        # Проверка сообщения об ошибке
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Ошибка при обработке товара, недостаточно на складе.")


    def test_purchase_create_view_invalid_stock(self):
        self.product.stock = 0
        self.product.save()

        response = self.client.post(
            reverse('buy', args=[self.product.id]),
            {'product': self.product.id, 'person': 'Test Person', 'address': 'Test Address'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "Товар недоступен для покупки, недостаточно на складе.")


    def test_purchase_create_view_invalid_form(self):
        
        response = self.client.post(reverse('buy', args=[self.product.id]), {})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('buy', args=[self.product.id]))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Ошибка валидации данных.")

    def test_purchase_create_view_no_product(self):
        response = self.client.post(reverse('buy', args=[999]))
        self.assertEqual(response.status_code, 302)
