from django.db import models
from django.contrib.auth.models import AbstractUser
from social_django.models import UserSocialAuth
from django.urls import reverse


class User(AbstractUser):
    avatar = models.ImageField(upload_to="users/%Y", default="default/avatar_icon.png", blank=True, null=True, verbose_name="Аватар")
    email_verify = models.BooleanField(default=False)
    

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        # Проверка, связан ли этот пользователь с аккаунтом социальной сети
        if UserSocialAuth.objects.filter(user=self).exists():
            self.email_verify = True
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:profile')