from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from course.models import Course


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
    )

    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    image_pic = models.FileField(upload_to='user_img/', null=True, blank=True)

    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class BookmarkBase(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class BookmarkCourse(BookmarkBase):
    class Meta:
        db_table = "bookmark_course"

    obj = models.ForeignKey(Course, verbose_name="Курс", on_delete=models.CASCADE)

