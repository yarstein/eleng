from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
]