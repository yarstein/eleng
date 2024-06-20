from django import template
from django.core.cache import cache
from news.models import News


register = template.Library()

@register.simple_tag
def get_latest_news():
    cached_news = cache.get('latest_news')
    if not cached_news:
        cached_news = News.objects.order_by('-time_create')[:4]
        cache.set('latest_news', cached_news, timeout=3600)  # Кешируем на 1 час
    return cached_news