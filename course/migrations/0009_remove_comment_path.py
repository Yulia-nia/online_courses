# Generated by Django 4.0.4 on 2022-05-13 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_rename_author_id_comment_author_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='path',
        ),
    ]
