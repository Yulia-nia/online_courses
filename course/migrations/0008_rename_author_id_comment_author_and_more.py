# Generated by Django 4.0.4 on 2022-05-13 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author_id',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='article_id',
            new_name='course',
        ),
    ]
