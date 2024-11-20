from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse
from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import Product, Purchase



def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        product = form.cleaned_data['product']
        
        if not product.is_available(1):
            messages.error(self.request, "Товар недоступен для покупки, недостаточно на складе.")
            return redirect('index')  # Перенаправление на главную страницу

        try:
            product.decrease_stock(1)
            self.object = form.save()
            messages.success(self.request, f"Спасибо за покупку, {self.object.person}!")
            return redirect('index')  # Перенаправление на главную страницу
        except ValueError:
            messages.error(self.request, "Ошибка при обработке товара, недостаточно на складе.")
            return redirect('index')  # Перенаправление на главную страницу
        
    def form_invalid(self, form):
        """Метод для обработки ошибок формы."""
        messages.error(self.request, "Ошибка валидации данных.")
        return redirect(self.request.path)
