# Generated by Django 4.0.3 on 2022-05-12 00:18

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0003_alter_file_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='module.block'),
        ),
        migrations.AlterField(
            model_name='text',
            name='content',
            field=tinymce.models.HTMLField(blank=True),
        ),
    ]
