# Generated by Django 4.2.7 on 2024-03-26 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_aboutcompany'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutcompany',
            name='main_image',
            field=models.ImageField(null=True, upload_to='main/', verbose_name='Изображение компании'),
        ),
    ]