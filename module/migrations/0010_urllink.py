# Generated by Django 4.0.4 on 2022-05-12 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0009_block_text_content_delete_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, null=True)),
                ('url', models.URLField()),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='module.block')),
            ],
            options={
                'verbose_name': ('Ссылка',),
                'verbose_name_plural': 'Ссылки',
                'db_table': 'url',
                'ordering': ('id',),
            },
        ),
    ]