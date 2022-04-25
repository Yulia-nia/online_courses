from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


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

