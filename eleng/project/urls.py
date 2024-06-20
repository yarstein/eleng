from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('product/', views.product, name='product'),
    path('aboutcompany/', views.aboutcompany, name='aboutcompany'),
    path('vacancy/', views.VacancyView.as_view(), name='vacancy'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]