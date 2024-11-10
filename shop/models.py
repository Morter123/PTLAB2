from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def is_available(self, quantity):
        """Проверка, есть ли достаточно товара на складе."""
        return self.stock >= quantity

    def decrease_stock(self, amount):
        """Уменьшаем количество товара на складе."""
        if self.stock >= amount:
            self.stock -= amount
            self.save()
        else:
            raise ValueError("Недостаточно товара на складе.")


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Перед сохранением уменьшаем количество товара на складе."""
        if self.product.is_available(1):  # Предполагаем, что покупается 1 товар
            self.product.decrease_stock(1)  # Уменьшаем количество на складе
            super().save(*args, **kwargs)
        else:
            raise ValueError(
                "Товар недоступен для покупки, недостаточно на складе.")
