# Generated by Django 4.0.3 on 2022-04-26 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0005_file_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='is_published',
            field=models.BooleanField(default=False, null=True),
        ),
    ]