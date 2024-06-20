from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField

from .utils import validate_phone_number

User = get_user_model()


class Slider(models.Model):
    """Модель для слайдера"""
    title = models.CharField(max_length=100, blank=False, verbose_name='Заголовок')
    description = models.TextField(max_length=500, blank=False, verbose_name='Описание')
    image = models.ImageField(upload_to='slider/', blank=False, verbose_name='Изображение')

    class Meta:
        ordering = ['pk']
        # отображение в админ.панели
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'
    
    def __str__(self):
        return self.title
    

class OurServices(models.Model):
    """Модель для описание наши услуги"""
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    summary = models.TextField(verbose_name='Краткое описание')
    content = models.TextField(verbose_name='Полное описание')
    summary_image = models.ImageField(upload_to='content/', blank=False, verbose_name='Изображение на главную страницу')
    content_image = models.ImageField(upload_to='content/', blank=False, verbose_name='Изображение для наши услуги')

    class Meta:
        ordering = ['pk']
        verbose_name = 'Наша услуга'
        verbose_name_plural = 'Наши услуги'

    def __str__(self):
        return self.title
    
# --------------------------------------------------------------------------------------------------
class AboutCompany(models.Model):
    """Модель для описание информации О компании"""
    content = RichTextField(blank=True, verbose_name='Текст о компании')
    main_image = models.ImageField(upload_to='company_images/', blank=True, null=True, verbose_name='Изображение компании')


    class Meta:
        verbose_name = 'О компании'
        verbose_name_plural = 'О компании'

    def __str__(self):
        return f'Информация о компании'
    

class CompanyFile(models.Model):
    """Модель для файлов компании"""
    company = models.ForeignKey(AboutCompany, related_name='files', on_delete=models.CASCADE, verbose_name='Компания')
    file = models.FileField(upload_to='company_files/', verbose_name='Файл')

    class Meta:
        verbose_name = 'Файл компании'
        verbose_name_plural = 'Файлы компании'

    def __str__(self):
        return self.file.name
    
    def is_pdf(self):
        return self.file.name.endswith('.pdf')
# --------------------------------------------------------------------------------------------------

class Vacancy(models.Model):
    """Модель для размещения вакансии"""
    title = models.CharField(max_length=150, verbose_name='Загаловок вакансии')
    description = RichTextField(verbose_name='Описание вакансии')
    
    class Meta:
        ordering = ['pk']
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return f'Вакансия №{self.pk}: {self.title}'
    

class Resume(models.Model):
    """Модель для закрепления резюме"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='Номер телефона', 
                                    validators=[validate_phone_number])
    email = models.EmailField(verbose_name='E-mail')
    resume_file = models.FileField(upload_to='resumes/', verbose_name='Резюме', 
                                   validators=[FileExtensionValidator(allowed_extensions=['pdf', 'djvu', 'doc', 'docx'])])
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки резюме')

    class Meta:
        ordering = ['pk']
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'


    def __str__(self):
        return f'Резюме от {self.first_name} {self.last_name}'
    

class Feedback(models.Model):
    """
    Модель обратной связи
    """
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    email = models.EmailField(max_length=100, verbose_name='Электронный адрес')
    content = models.TextField(verbose_name='Содержимое письма')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    ip_address = models.GenericIPAddressField(verbose_name='IP отправителя', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-time_create']

    def __str__(self):
        return f'Вам письмо от {self.email}'