from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from catalog.models import Article
from .cart import Cart
from .forms import CartAddProductForm


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'title': 'Корзина'})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Article.objects.select_related('category'), id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity = cd['quantity'], override_quantity=cd['override'])

    return redirect(request.META['HTTP_REFERER'])
        

@require_POST
def cart_delete(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Article.objects.select_related('category'), id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

