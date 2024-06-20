# Generated by Django 4.2.7 on 2024-03-29 10:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_resume_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='resume_file',
            field=models.FileField(upload_to='resumes/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'djvu', 'doc', 'docx'])], verbose_name='Резюме'),
        ),
    ]