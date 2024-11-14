from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
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
            return HttpResponseBadRequest("Товар недоступен для покупки, недостаточно на складе.")

        try:
            product.decrease_stock(1)
            self.object = form.save()
            return HttpResponse(f'Спасибо за покупку, {self.object.person}!')
        except ValueError:
            return HttpResponseBadRequest("Товар недоступен для покупки, недостаточно на складе.")
        
    def form_invalid(self, form):
        """Метод для обработки ошибок формы."""
        return HttpResponseBadRequest("Ошибка валидации данных.")
