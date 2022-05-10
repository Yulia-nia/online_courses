from django.db import models

# Create your models here.
import course.models
from users.models import User


class Module(models.Model):
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE)
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
    is_published = models.BooleanField(null=True, default=False)

    class Meta:
        ordering = ('id',)
        db_table = 'lesson'
        verbose_name = 'Урок',
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class Block(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
        db_table = 'block'
        verbose_name = 'Блок урока',
        verbose_name_plural = 'Блоки урока'

    def __str__(self):
        return self.title


class Text(models.Model):
    content = models.TextField(null=True, blank=True)
    time_update = models.DateTimeField(auto_now=True)
    time_create = models.DateTimeField(auto_now_add=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        db_table = 'text'
        verbose_name = 'Текс',
        verbose_name_plural = 'Текста'

    def __str__(self):
        return self.content


class File(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    file = models.FileField(upload_to='files/%Y-%m-%d/', null=True, blank=True)
    time_update = models.DateTimeField(auto_now=True)
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
        db_table = 'files'
        verbose_name = 'Файл',
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.title


class Task(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_deadline = models.DateTimeField(null=True)
    file = models.FileField(upload_to='files/%Y-%m-%d/', null=True, blank=True)

    class Meta:
        ordering = ('id',)
        db_table = 'task'
        verbose_name = 'Задание',
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.title


class StudentAnswer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='files/%Y-%m-%d/', null=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)
        db_table = 'student_answer'
        verbose_name = 'Ответ на задание',
        verbose_name_plural = 'Ответы на задания'

    def __str__(self):
        return self.student.email


class Mark(models.Model):
    answer = models.OneToOneField(StudentAnswer, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)
    mark = models.IntegerField(null=True)

    class Meta:
        ordering = ('id',)
        db_table = 'mark'
        verbose_name = 'Оценка',
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return self.mark


class Announcement(models.Model):
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE)
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

