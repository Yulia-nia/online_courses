# Generated by Django 4.0.4 on 2022-05-12 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0008_alter_text_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='text_content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Text',
        ),
    ]
