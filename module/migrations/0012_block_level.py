# Generated by Django 4.0.4 on 2022-05-29 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0011_alter_announcement_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='level',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]