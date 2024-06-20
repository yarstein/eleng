from django.conf import settings

from .forms import CartAddProductForm
from catalog.models import Article


class Cart:

    def __init__(self, request):

        # текущая сессия
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart
        self.products = None  # Кэш продуктов


    def load_products(self):
        """ Загрузка и кэширование продуктов из базы данных один раз. """
        if self.products is None:
            product_ids = self.cart.keys()
            self.products = Article.objects.filter(id__in=product_ids).select_related('category')
            self.products = {str(product.id): product for product in self.products}
        return self.products
    

    def __iter__(self):
        """ Итерация по товарам в корзине с использованием кэшированных данных. """
        products = self.load_products()
        for product_id, data in self.cart.items():
            product = products.get(product_id)
            if product:
                # Создание формы для каждого товара
                form = CartAddProductForm(initial={'quantity': data['quantity'], 'override': True})
                yield {'quantity': data['quantity'], 'update_quantity_form': form, 'product': product}

    
    # def __iter__(self):
    #     """Прокрутить товарные позиции корзины в цикле и получить товары из БД"""

    #     product_ids = self.cart.keys()
    #     products = Article.objects.filter(id__in=product_ids).select_related('category')
    #     cart = self.cart.copy()

    #     for product in products:
    #         cart[str(product.id)]['product'] = product
    #     for item in cart.values():
    #         yield item
            


    def __len__(self):
        """Подсчитать все товарные позиции в корзине"""

        return sum(item['quantity'] for item in self.cart.values())

    
    def add(self, product, quantity=1, override_quantity=False):
        """Добавить товар в корзину либо обновить его количество"""
        
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    
    def save(self):
        """Пометить сессию как измененный, чтобы обеспечить его сохранение"""
        self.session.modified = True


    def remove(self, product):
        """Удалить товар из корзины"""

        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """Удалить корзину из сессии"""
        del self.session[settings.CART_SESSION_ID]
        self.save()