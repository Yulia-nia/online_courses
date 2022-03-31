from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)   # empty values
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_update = models.DateTimeField(auto_now=True)
    time_create = models.DateTimeField(auto_now_add=True)         # value does not change

    class Meta:
        ordering = ('title',)
        db_table = 'course'
        verbose_name = 'Курс',
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Settings(models.Model):
    learning_format = models.CharField(max_length=200, null=True)
    subject = models.CharField(max_length=200, null=True)
    language = models.CharField(max_length=200, null=True)
    course = models.OneToOneField(Course, on_delete=models.CASCADE, primary_key=True)
    # изображение (должно быть, установить сначала дефолтное)
    # picture =
    # обложка
    # background_image =

    class Meta:
        db_table = 'settings'
        verbose_name = 'Основные настройки',
        verbose_name_plural = 'Основные настройки'


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # description = models.TextField(null=True, blank=True)  # empty values
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title',)
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

    short_description = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ('title',)
        db_table = 'lesson'
        verbose_name = 'Урок',
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title