from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
# Create your views here.
from course.models import Course
from module.forms import ModuleForm, AnnouncementForm
from module.models import Module, Lesson, Announcement
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def list_module(request, id):
    course = Course.objects.get(id=id)
    form = ModuleForm()
    modules = Module.objects.all()
    #form_announcement = AnnouncementForm()

    #announcements = Announcement.objects.all().filter(course_id=id)

    #count_list = zip(announcements, range(1, announcements.count()+1))
    # in case to filter by id
    modules = Module.objects.filter(course_id=id)
    lessons = Lesson.objects.all().filter(module__course_id=id)
    return render(request, "module/module_list.html", {"form": form, "modules": modules,
                                                       # "form_announcement": form_announcement,
                                                       # "announcements": announcements,
                                                       # "count_list": count_list,
                                                       "course": course, "lessons": lessons, "item_id": id})


def create_module(request, id):
    if request.method == "POST":
        module = Module()
        module.title = request.POST.get("title")
        module.course_id = id
        module.save()
    return HttpResponseRedirect(reverse('list', args=(id,)))


def create_lesson(request, id):
    lesson = Lesson()
    if request.method == "POST":
        lesson.title = request.POST.get("title")
        lesson.short_description = request.POST.get("short_description")
        lesson.description = request.POST.get("description")
        lesson.module_id = id
        lesson.save()
    return render(request, "module/create_lesson.html", {"lesson": lesson, "item_id": id})


def edit_lesson(request, id):
    try:
        lesson = Lesson.objects.get(id=id)
        if request.method == "POST":
            lesson.title = request.POST.get("title")
            lesson.short_description = request.POST.get("short_description")
            lesson.description = request.POST.get("description")
            lesson.save()
            return render(request, "module/edit_lesson.html", {"lesson": lesson, "item_id": id})
        else:
            return render(request, "module/edit_lesson.html", {"lesson": lesson, "item_id": id})
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>Lesson not found</h2>")


def edit_module(request, id):
    try:
        module = Module.objects.get(id=id)
        course = Course.objects.get(id=module.course_id)
        lessons = Lesson.objects.all().filter(module_id=id)
        return render(request, "module/edit_module.html", {"module": module, "lessons": lessons, "module_id": id})
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>Module not found</h2>")


def edit_lesson_from_module(request, module_id, id):
    try:
        lesson = Lesson.objects.get(id=id)
        if request.method == "POST":
            lesson.title = request.POST.get("title")
            lesson.short_description = request.POST.get("short_description")
            lesson.description = request.POST.get("description")
            lesson.save()
            return render(request, "module/edit_lesson.html", {"lesson": lesson, "item_id": id})
        else:
            return render(request, "module/edit_lesson.html", {"lesson": lesson, "item_id": id})
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>Lesson not found</h2>")