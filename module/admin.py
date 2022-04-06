from django.contrib import admin
# Register your models here.
from .models import Module, Lesson


admin.site.register(Module)
admin.site.register(Lesson)