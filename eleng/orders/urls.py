from django.urls import path

from . import views


urlpatterns = [
    path('', views.order_create, name='order_create'),
    path('order_complete/', views.order_complete, name='order_complete'),
]