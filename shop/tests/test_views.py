from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Purchase


class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="Book", price=740, stock=1)


def test_purchase_success_when_stock_available(self):
    """Проверка успешной покупки, если товар в наличии."""
    response = self.client.post(reverse('buy', args=[self.product.id]), {
        'person': 'Покупатель',
        'address': 'Светлый путь, 10'
    })
    self.product.refresh_from_db()  # Обновляем объект из базы данных
    self.assertEqual(self.product.stock, 0)  # Товар должен уменьшиться на 1
    self.assertEqual(response.status_code, 200)  # Ожидаем успешный ответ
    # Проверка успешного сообщения
    self.assertContains(response, 'Спасибо за покупку')


def test_invalid_purchase_person(self):
    """Проверка, что покупка не пройдет при некорректном имени."""
    response = self.client.post(reverse('buy', args=[self.product.id]), {
        'person': '---',  # Некорректное имя
        'address': 'Street Test'
    })
    self.assertEqual(response.status_code, 400)  # Ожидаем ошибку
    self.assertContains(response, 'Имя должно содержать только буквы.')


def test_invalid_purchase_address(self):
    """Проверка, что покупка не пройдет при некорректном адресе."""
    response = self.client.post(reverse('buy', args=[self.product.id]), {
        'person': 'Buyer',
        'address': '-12'  # Некорректный адрес
    })
    self.assertEqual(response.status_code, 400)  # Ожидаем ошибку
    self.assertContains(response, 'Адрес содержит некорректные символы.')


def test_purchase_fails_when_no_stock_available(self):
    """Проверка, что покупка не удастся, если товара нет в наличии."""
    self.product.stock = 0
    self.product.save()
    response = self.client.post(reverse('buy', args=[self.product.id]), {
        'person': 'Petrov',
        'address': 'Dark Road'
    })
    self.assertEqual(response.status_code, 400)  # Ожидаем ошибку
    self.assertContains(
        response, 'Товар недоступен для покупки, недостаточно на складе.')
