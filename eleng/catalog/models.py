from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.contrib.auth import get_user_model

from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField


User = get_user_model()

class Article(models.Model):

    class Status(models.IntegerChoices):
        """Перечисление статусов в форме. 0 и 1 значения записываются в БД, Черновик и Опубликовано в форме"""
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    name = models.CharField(max_length=255, verbose_name="Изделие")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = RichTextField(blank=True, verbose_name='Описание')
    characteristics = RichTextField(blank=True, verbose_name='Характеристики')
    photo = models.ImageField(upload_to='photos/%Y/%m', default="default/No_photo.png", blank=True, null=True, verbose_name='Фото',
                              validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg'))])
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), 
                                       default=Status.PUBLISHED, verbose_name='Статус')
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='articles', verbose_name='Категория')
    tags = models.ManyToManyField('TagProduct', blank=True, related_name='product_tags', verbose_name='Теги')


    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['slug', '-time_create'])
        ]
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталог'


    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        return reverse('catalog_detail', kwargs={'arc_slug':self.slug})
    


class Category(MPTTModel):
    """
    Модель категорий с вложенностью
    """
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL категории')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', 
                            verbose_name='Родительская категория')

    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('title',)


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('catalog_by_category', kwargs={'slug': self.slug})
    

class Comment(MPTTModel):
    """
    Модель древовидных комментариев
    """

    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    product = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Изделие', related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', related_name='comments_author')
    content = models.TextField(verbose_name='Текст комментария', max_length=3000)
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус поста', max_length=10)
    parent = TreeForeignKey('self', verbose_name='Родительский комментарий', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class MTTMeta:
        order_insertion_by = ('-time_create',)
    
    class Meta:
        db_table = 'app_comments'
        indexes = [models.Index(fields=['-time_create', 'time_update', 'status', 'parent'])]
        ordering = ['-time_create']
        verbose_name = 'Комментарий в Каталоге'
        verbose_name_plural = 'Комментарии в Каталоге'

    def __str__(self):
        return f'{self.author}:{self.content}'


class TagProduct(models.Model):
    tag = models.CharField(max_length=150, db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name="URL")


    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    
    def __str__(self):
        return self.tag
    
    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})
