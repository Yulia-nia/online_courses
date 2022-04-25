from django.contrib import admin
# Register your models here.
from .models import Module, Lesson, Announcement, File


admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Announcement)
admin.site.register(File)