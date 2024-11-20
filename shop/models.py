from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def is_available(self, quantity):
        """Проверка, есть ли достаточно товара на складе."""
        return self.stock >= quantity

    def decrease_stock(self, amount):
        """Уменьшаем количество товара на складе и сохраняем его."""
        if self.stock >= amount:
            self.stock -= amount
            self.save()  # Сохраняем изменения в базе данных
        else:
            raise ValueError("Недостаточно товара на складе.")

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(1, "Имя не может быть пустым."),
            RegexValidator(r'^[a-zA-Zа-яА-ЯёЁ\s]+$', "Имя должно содержать только буквы."),
        ],
    )
    address = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(1, "Адрес не может быть пустым."),
            RegexValidator(r'^[\w\s,-]+$', "Адрес содержит некорректные символы."),
        ],
    )
    date = models.DateTimeField(auto_now_add=True)