from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)   # empty values
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_update = models.DateTimeField(auto_now=True)
    time_create = models.DateTimeField(auto_now_add=True)         # value does not change

    class Meta:
        ordering = ('id',)
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
