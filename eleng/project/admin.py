from django.contrib import admin
from django.utils.safestring import mark_safe   # ф-я, которая не экранирует html-теги
from django.utils.html import format_html

from .models import Slider, OurServices, AboutCompany, CompanyFile, Vacancy, Resume, Feedback


@admin.register(Slider)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slider_photo')
    list_display_links = ('pk', 'title',)

    @admin.display(description='Фото в слайде')
    def slider_photo(self, slide: Slider):
        if slide.image:
            return mark_safe(f"<img src='{slide.image.url}' width=50>")

@admin.register(OurServices)
class OurServicesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'summary_image_photo', 'content_image_photo')
    list_display_links = ('pk', 'title')

    @admin.display(description='Фото на главной странице')
    def summary_image_photo(self, image: OurServices):
        if image.summary_image:
            return mark_safe(f"<img src='{image.summary_image.url}' width=50>")
        
    @admin.display(description='Фото наши услуги')
    def content_image_photo(self, image: OurServices):
        if image.content_image:
            return mark_safe(f"<img src='{image.content_image.url}' width=50>")


class CompanyFileInline(admin.TabularInline):
    model = CompanyFile
    extra = 1  # Количество пустых форм для файлов

@admin.register(AboutCompany)
class AboutCompanyAdmin(admin.ModelAdmin):
    inlines = [CompanyFileInline,]


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'phone_number', 'email', 'resume_file', 'created')


admin.site.register(Vacancy)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = ('pk', 'short_content', 'email', 'ip_address', 'user')
    list_display_links = ('pk', 'email', 'ip_address')

    def short_content(self, obj):
        """
        Отображает первые 100 символов поля content.
        """
        return format_html('<span title="{}">{}</span>', obj.content, obj.content[:100] + '...' if len(obj.content) > 100 else obj.content)
    
    short_content.short_description = "Краткое содержание"