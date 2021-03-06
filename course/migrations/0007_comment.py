# Generated by Django 4.0.4 on 2022-05-13 22:30

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0006_rename_tieme_create_coursenrollment_time_create_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('content', models.TextField(blank=True, verbose_name='Комментарий')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('author_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': ('Комментарий',),
                'verbose_name_plural': 'Комментарии',
                'db_table': 'comments',
            },
        ),
    ]
