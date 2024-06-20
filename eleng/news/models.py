from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model

User = get_user_model()


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name="URL")
    image = models.ImageField(upload_to='news/%Y/%m', verbose_name='Изображение')
    content = RichTextUploadingField(verbose_name='Содержание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        ordering = ['-time_create']
        indexes = [models.Index(fields=['slug', '-time_create'])]
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return f'{self.pk}: {self.title}'
    
    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug':self.slug})
