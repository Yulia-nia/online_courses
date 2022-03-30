from django.db import models


# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)   # empty values
    # courses =         # list of courses
    # countCourses =
    time_update = models.DateTimeField(auto_now=True)
    time_create = models.DateTimeField(auto_now_add=True)         # value does not change

    class Meta:
        ordering = ('title',)
        db_table = 'subject'
        verbose_name = 'Предмет',
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)  # empty values
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title',)
        db_table = 'course'
        verbose_name = 'Курс',
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name