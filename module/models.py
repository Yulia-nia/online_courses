from django.db import models

# Create your models here.
from course.models import Course


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # description = models.TextField(null=True, blank=True)  # empty values
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
        db_table = 'module'
        verbose_name = 'Модуль',
        verbose_name_plural = 'Модули'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)
    short_description = models.TextField(max_length=250)
    description = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ('id',)
        db_table = 'lesson'
        verbose_name = 'Урок',
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class Announcement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    # description = models.TextField(null=True, blank=True)  # empty values
    time_update = models.DateTimeField(auto_now=True)
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
        db_table = 'announcement'
        verbose_name = 'Обявление',
        verbose_name_plural = 'Объявление'

    def __str__(self):
        return self.content


class File(models.Model):
    title = models.CharField(max_length=250)
    file = models.FileField(upload_to='files/%Y-%m-%d/', null=True, blank=True)
    time_update = models.DateTimeField(auto_now=True)
    time_create = models.DateTimeField(auto_now_add=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        db_table = 'files'
        verbose_name = 'Файл',
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.title