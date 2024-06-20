from django.contrib import admin
from django.utils.safestring import mark_safe   # ф-я, которая не экранирует html-теги
from mptt.admin import DraggableMPTTAdmin
from .models import Article, Category, Comment, TagProduct


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """
    Админ-панель модели категорий
    """
    list_display = ('tree_actions', 'indented_title', 'id', 'slug')
    list_display_links = ('indented_title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

    # fieldsets = (
    #     ('Основная информация', {'fields': ('title', 'slug', 'parent')}),
    # )

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'category', 'name', 'is_published', 'product_photo')
    list_display_links = ('pk', 'name', 'product_photo')
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description='Фото')
    def product_photo(self, image: Article):
        if image.photo:
            return mark_safe(f"<img src='{image.photo.url}' width=50>")


@admin.register(TagProduct)
class TagProductAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {'slug': ('tag',)}
    

@admin.register(Comment)
class CommentAdminPage(DraggableMPTTAdmin):
    """
    Админ-панель модели комментариев
    """
    list_display = ('pk', 'tree_actions', 'indented_title', 'product', 'author', 'time_create', 'status')
    # mptt_level_indent = 2
    list_display_links = ('product',)
    list_filter = ('time_create', 'time_update', 'author')
    list_editable = ('status',)