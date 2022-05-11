# Generated by Django 4.0.3 on 2022-05-10 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': ('Курс',),
                'verbose_name_plural': 'Курсы',
                'db_table': 'course',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('time_create', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': ('Уведомление',),
                'verbose_name_plural': 'Уведомления',
                'db_table': 'notifications',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('learning_format', models.CharField(max_length=200, null=True)),
                ('subject', models.CharField(max_length=200, null=True)),
                ('language', models.CharField(max_length=200, null=True)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='course.course')),
                ('image', models.FileField(blank=True, null=True, upload_to='course_img/')),
                ('is_published', models.BooleanField(default=False, null=True)),
                ('will_learn', models.TextField(blank=True, null=True)),
                ('about_course', models.TextField(blank=True, null=True)),
                ('necessary_training', models.TextField(blank=True, null=True)),
                ('how_training', models.TextField(blank=True, null=True)),
                ('what_you_get', models.TextField(blank=True, null=True)),
                ('level', models.CharField(choices=[('1', 'для начаниющих'), ('2', 'для продолжающих'), ('3', 'для продвинутых')], default='1', max_length=1, verbose_name='уровень')),
            ],
            options={
                'verbose_name': ('Основные настройки',),
                'verbose_name_plural': 'Основные настройки',
                'db_table': 'settings',
            },
        ),
        migrations.CreateModel(
            name='РassingРrogress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_pass', models.BooleanField(default=False, null=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
            ],
            options={
                'verbose_name': ('Прогресс прохождения',),
                'verbose_name_plural': 'Прогресс прохождения',
                'db_table': 'passing_progress',
            },
        ),
    ]
