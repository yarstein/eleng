# Generated by Django 4.2.7 on 2024-03-07 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_tagproduct_alter_comment_options_article_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tagproduct',
            options={'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
    ]
