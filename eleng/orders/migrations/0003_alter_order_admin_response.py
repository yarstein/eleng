# Generated by Django 4.2.7 on 2024-03-19 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_admin_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='admin_response',
            field=models.TextField(blank=True, verbose_name='Сообщение от администратора'),
        ),
    ]