from django.contrib import admin
from django.urls import path, include
from eleng import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from project.sitemaps import NewsSitemap, CategorySitemap, ProductSitemap, StaticViewSitemap

sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'news': NewsSitemap,
    'static': StaticViewSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('catalog/', include('catalog.urls')),
    path('news/', include('news.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('captcha/', include('captcha.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]

# В режиме отладки добавляем новый маршрут. Префикс MEDIA_URL свяжем с маршрутом document_root, который указан в корневом каталоге media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)