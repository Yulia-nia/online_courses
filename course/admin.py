from django.contrib import admin
# Register your models here.
from .models import Course, Settings, РassingРrogress  #, Module, Lesson


admin.site.register(Course)
admin.site.register(Settings)
admin.site.register(РassingРrogress)
# admin.site.register(Module)
# admin.site.register(Lesson)