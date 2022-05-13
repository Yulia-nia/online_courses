from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import FileSystemStorage
from django.db import models

from module.models import Lesson
from online_courses import settings
from users.models import User


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
    image = models.FileField(upload_to='course_img/', null=True, blank=True)
    is_published = models.BooleanField(null=True, default=False)

    is_active = models.BooleanField(null=True, default=False)  # start or end
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    # recruitment_start_date = models.DateTimeField(null=True)

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

    COURSE_CHOICES = (
        ('0', "идет разработка курса"),
        ('1', "идет набор на курс"),
        ('2', "курс начался"),
        ('3', "курс закончился"),
    )
    active_level = models.CharField(max_length=1, verbose_name="статус курса", choices=COURSE_CHOICES, default='0')
    level = models.CharField(max_length=1, verbose_name="уровень", choices=LEVEL_CHOICES, default='1')

    class Meta:
        db_table = 'settings'
        verbose_name = 'Основные настройки',
        verbose_name_plural = 'Основные настройки'


class РassingРrogress(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    is_pass = models.BooleanField(null=True, default=False)
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'passing_progress'
        verbose_name = 'Прогресс прохождения',
        verbose_name_plural = 'Прогресс прохождения'

    def __str__(self):
        return self.student.email


class Notifications(models.Model):
    content = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    time_create = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Уведомление',
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return self.content


class CoursEnrollment(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, primary_key=True)
    students = models.ManyToManyField(User)
    time_create = models.DateTimeField(auto_now_add=True)
    time_end = models.DateTimeField(null=True)

    class Meta:
        db_table = ' course_enrollment'
        verbose_name = 'Набор на курс',
        verbose_name_plural = 'Набор на курс'


class Comment(models.Model):
    # path = ArrayField(models.IntegerField())
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField('Комментарий', blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comments"
        verbose_name = 'Комментарий',
        verbose_name_plural = 'Комментарии'

    def  __str__(self):
        return self.content[0:200]

    # def get_offset(self):
    #     level = len(self.path) - 1
    #     if level > 5:
    #         level = 5
    #     return level
    #
    # def get_col(self):
    #     level = len(self.path) - 1
    #     if level > 5:
    #         level = 5
    #     return 12 - level

