# Generated by Django 4.2.7 on 2024-03-29 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_alter_resume_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=None, verbose_name='Время отправки резюме'),
            preserve_default=False,
        ),
    ]
