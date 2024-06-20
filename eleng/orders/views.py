from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             # Теперь создаем OrderItem для каждого товара в корзине
#             for item in cart:
#                 OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'])
#             # очистить корзину
#             cart.clear()
#             return render(request, 'orders/create_orders.html', {'order': order})
#     else:
#         initial = {
#             'username': request.user.username,
#             'email': request.user.email,
#             'first_name': request.user.first_name,
#             'last_name': request.user.last_name
#             }
#         form = OrderCreateForm(initial=initial)
#     return render(request, 'orders/create_orders.html', {'form': form})


@login_required(login_url='users:login')
def order_create(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.error(request, 'Ваша корзина пуста, добавьте товары перед оформлением заказа.')
        return redirect('cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
                order.save()
                for item in cart:
                    OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'])
                cart.clear()
                return redirect('order_complete')
            else:
                messages.info(request, 'Пожалуйста, зарегистрируйтесь или войдите, чтобы совершить покупку.')
                return redirect('users:login')
    else:
        if request.user.is_authenticated:
            form = OrderCreateForm(user=request.user)
        else:
            messages.info(request, 'Пожалуйста, зарегистрируйтесь или войдите, чтобы продолжить покупку.')
            return redirect('users:login')
    return render(request, 'orders/create_orders.html', {'form': form, 'title':'Оформление заказа'})


def order_complete(request):
    return render(request, 'orders/order_complete.html', {'title':'Заказ оформлен'})