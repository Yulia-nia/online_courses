from django.db import models


# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)   # empty values
    # courses =         # list of courses
    # countCourses =
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)         # value does not change

    class Meta:
        ordering = ('name',)
        verbose_name = 'Предмет',
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name