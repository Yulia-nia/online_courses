from django.contrib import admin
# Register your models here.
from .models import Module, Lesson, Announcement, File, Task, StudentAnswer, Mark, Block


admin.site.register(Module)
admin.site.register(Lesson)
# admin.site.register(Text)
admin.site.register(Task)
admin.site.register(StudentAnswer)
admin.site.register(Mark)
admin.site.register(Announcement)
admin.site.register(File)
admin.site.register(Block)
