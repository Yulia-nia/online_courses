from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect

# Create your views here.
from course.forms import CourseForm
from course.models import Course, Settings


def index(request):
    courseform = CourseForm()
    courses = Course.objects.all()
    return render(request, "course/index.html", {"form": courseform, "courses": courses})


def settings_edit(request, id):
    try:
        setting = Settings.objects.get(course_id=id)
        if request.method == "POST":
            setting.learning_format = request.POST.get("learning_format")
            setting.subject = request.POST.get("subject")
            setting.language = request.POST.get("language")
            setting.save()
        return render(request, "course/main_settings.html", {"setting": setting, "item_id": id})
    except Settings.DoesNotExist:
        setting1 = Settings()
        if request.method == "POST":
            setting1.learning_format = request.POST.get("learning_format")
            setting1.subject = request.POST.get("subject")
            setting1.language = request.POST.get("language")
            setting1.course_id = id
            setting1.save()
        return render(request, "course/main_settings.html", {"setting": setting1, "item_id": id})

def create_course(request):
    if request.method == "POST":
        course = Course()
        course.title = request.POST.get("title")
        course.description = request.POST.get("description")
        course.save()
    return HttpResponseRedirect("/")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def edit_course(request, id):
    try:
        course = Course.objects.get(id=id)
        if request.method == "POST":
            course.title = request.POST.get("title")
            course.description = request.POST.get("description")
            course.save()
            return render(request, "course/edit_course.html", {"course": course, "item_id": id})
        else:
            return render(request, "course/edit_course.html", {"course": course, "item_id": id})
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>Course not found</h2>")


def delete_course(request, id):
    try:
        course = Course.objects.get(id=id)
        course.delete()
        return HttpResponseRedirect("/")
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>Course not found</h2>")
