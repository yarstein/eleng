from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from catalog.models import Article, Category
from news.models import News



class ProductSitemap(Sitemap):
    """
    Карта-сайта для изделий
    """
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Article.objects.filter(is_published=True)
    
    def lastmod(self, obj):
        return obj.time_update
    

class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    protocol = 'https'

    def items(self):
        return Category.objects.all()
    

class NewsSitemap(Sitemap):
    """
    Карта-сайта для новостей
    """
    changefreq = "monthly"
    priority = 0.5
    protocol = 'https'


    def items(self):
        return News.objects.all()
    

class StaticViewSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return ['home', 'product', 'aboutcompany', 'vacancy', 'contact']

    def location(self, item):
        return reverse(item)