# Generated by Django 4.0.3 on 2022-05-10 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=250)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': ('Обявление',),
                'verbose_name_plural': 'Объявление',
                'db_table': 'announcement',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('create', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': ('Блок урока',),
                'verbose_name_plural': 'Блоки урока',
                'db_table': 'block',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('file', models.FileField(blank=True, null=True, upload_to='files/%Y-%m-%d/')),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': ('Файл',),
                'verbose_name_plural': 'Файлы',
                'db_table': 'files',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('update', models.DateTimeField(auto_now=True)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('short_description', models.TextField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_published', models.BooleanField(default=False, null=True)),
            ],
            options={
                'verbose_name': ('Урок',),
                'verbose_name_plural': 'Уроки',
                'db_table': 'lesson',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('mark', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name': ('Оценка',),
                'verbose_name_plural': 'Оценки',
                'db_table': 'mark',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('update', models.DateTimeField(auto_now=True)),
                ('create', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': ('Модуль',),
                'verbose_name_plural': 'Модули',
                'db_table': 'module',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='files/%Y-%m-%d/')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': ('Ответ на задание',),
                'verbose_name_plural': 'Ответы на задания',
                'db_table': 'student_answer',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='module.block')),
            ],
            options={
                'verbose_name': ('Текс',),
                'verbose_name_plural': 'Текста',
                'db_table': 'text',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_deadline', models.DateTimeField(null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='files/%Y-%m-%d/')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='module.module')),
            ],
            options={
                'verbose_name': ('Задание',),
                'verbose_name_plural': 'Задания',
                'db_table': 'task',
                'ordering': ('id',),
            },
        ),
    ]
