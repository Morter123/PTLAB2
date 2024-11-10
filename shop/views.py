from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .models import Product, Purchase

# Create your views here.


def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        product = form.cleaned_data['product']
        if product.stock < 1:
            return HttpResponseBadRequest("Товар недоступен для покупки, недостаточно на складе.")

        # Если товар доступен, уменьшаем его количество
        product.decrease_stock(1)
        self.object = form.save()
        return HttpResponse(f'Спасибо за покупку, {self.object.person}!')