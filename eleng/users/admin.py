from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from users.models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('pk', 'username', 'first_name', 'last_name', 'email', 'email_verify', 'get_avatar')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {'fields': ('avatar', 'email_verify')}),
    )
    ordering = ('pk',)  # Добавляем сортировку по username

    def get_avatar(self, obj):
        return format_html('<img src="{}" style="width: 45px; height:45px;" />', obj.avatar.url) if obj.avatar else 'No image'

    get_avatar.short_description = 'Avatar'

admin.site.register(User, CustomUserAdmin)