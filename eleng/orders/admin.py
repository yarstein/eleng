from django.contrib import admin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, reverse
from django.core.mail import send_mail
from django.utils.html import format_html, mark_safe

from .models import Order, OrderItem
from .forms import ResponseForm
from eleng import settings
from .tasks import send_response_email


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone_number', 'comments', 'respond', 'city', 'status', 'created']
    inlines = [OrderItemInline]
    exclude = ('admin_response',)

# ----------------------------
    readonly_fields = ['admin_response_display',]

    def admin_response_display(self, obj):
        return mark_safe(obj.admin_response)
    admin_response_display.short_description = "Ответ администратора"
# ---------------------------------------------

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:order_id>/respond/', self.admin_site.admin_view(self.respond_to_user), name='order-respond'),
        ]
        return custom_urls + urls
    
    def respond(self, obj):
        return format_html('<a class="button" href="{}">Ответить</a> ', reverse('admin:order-respond', args=[obj.pk])) 
    respond.short_description = 'Ответить'
    respond.allow_tags = True

    def respond_to_user(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id)

        if request.method == 'POST':
            form = ResponseForm(request.POST)
            if form.is_valid():
                message = form.cleaned_data['admin_response']
                subject = f'Ответ на ваш заказ №{order.id}'
                email_from = settings.DEFAULT_FROM_EMAIL
                recipient_list = [order.user.email]
                
                # try:
                #     send_mail(subject, message, email_from, recipient_list, html_message=message, fail_silently=False)
                #     self.message_user(request, 'Вы успешно отправили письмо.')

                #     # Обновляем статус заказа и сохраняем ответ администратора в БД
                #     if not order.status:
                #         order.status = True
                #         order.admin_response = message
                #         order.save()

                # except Exception as e:
                #     self.message_user(request, f'Ошибка при отправке письма: {e}')

                # Используем Celery для отправки письма
                send_response_email.delay(subject, message, recipient_list)
                self.message_user(request, 'Вы успешно отправили письмо.')

                # Обновляем статус заказа и сохраняем ответ администратора в БД
                if not order.status:
                    order.status = True
                    order.admin_response = message
                    order.save()

                # url = reverse('admin:orders_order_change', args=[order.pk], current_app=self.admin_site.name)
                url = reverse('admin:orders_order_changelist')
                return redirect(url)
        else:
            form = ResponseForm()

        context = dict(
           self.admin_site.each_context(request),
           form=form,
           order=order
        )
        return render(request, 'admin/orders/respond_to_user.html', context)