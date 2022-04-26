from django.core.files.storage import FileSystemStorage
from django.db import models

from online_courses import settings


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)   # empty values
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    # logo
    image = models.FileField(upload_to='course_img/', null=True, blank=True)
    is_published = models.BooleanField(null=True, default=False)

    will_learn = models.TextField(null=True, blank=True)
    about_course = models.TextField(null=True, blank=True)
    necessary_training = models.TextField(null=True, blank=True)
    how_training = models.TextField(null=True, blank=True)
    what_you_get = models.TextField(null=True, blank=True)

    LEVEL_CHOICES = (
        ('1', "для начаниющих"),
        ('2', "для продолжающих"),
        ('3', "для продвинутых"),
    )
    level = models.CharField(max_length=1, verbose_name="уровень", choices=LEVEL_CHOICES, default='1')
    # (?) video =

    class Meta:
        db_table = 'settings'
        verbose_name = 'Основные настройки',
        verbose_name_plural = 'Основные настройки'
