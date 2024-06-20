from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.cache import cache

from .models import News



class NewsListView(ListView):
    """Представление для списка новостей"""
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости'
        return context

    def get_queryset(self):
        news_list = cache.get('news_list')
        if not news_list:
            news_list = super().get_queryset()
            cache.set('news_list', news_list, 3600)
        return news_list


class NewsDetailView(DetailView):
    """Представление для детальной информации о новостях"""
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context
