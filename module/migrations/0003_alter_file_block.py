# Generated by Django 4.0.3 on 2022-05-12 00:05

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='block',
            field=tinymce.models.HTMLField(),
        ),
    ]
