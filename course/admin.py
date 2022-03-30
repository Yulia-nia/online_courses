from django.contrib import admin
# Register your models here.
from .models import Subject, Course


admin.site.register(Subject)
admin.site.register(Course)