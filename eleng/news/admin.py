from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'title_image', 'time_create')
    list_display_links = ('pk', 'title',)
    prepopulated_fields = {'slug': ('title',)}

    @admin.display(description='Фото на заголовке')
    def title_image(self, photo: News):
        if photo.image:
            return mark_safe(f"<img src='{photo.image.url}' width=50>")
