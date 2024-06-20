from django.contrib.auth import get_user_model
from django.db import models
from ckeditor.fields import RichTextField

from catalog.models import Article
from project.utils import validate_phone_number

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='Номер телефона', validators=[validate_phone_number])
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')
    comments = models.TextField(max_length=3000, blank=True, verbose_name='Коментарий к заказу')
    status = models.BooleanField(default=False, verbose_name='Обработан')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    admin_response = models.TextField(blank=True, verbose_name='Сообщение от администратора')

    class Meta:
        db_table = 'order'
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Article, related_name='order_items', on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
            db_table = 'order_item'
            verbose_name = 'Товар'
            verbose_name_plural = 'Товары'

    def __str__(self):
        return str(self.pk)