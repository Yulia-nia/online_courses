from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect

# Create your views here.
from course.forms import CourseForm
from course.models import Course


def index(request):
    courseform = CourseForm()
    return render(request, "course/index.html", {"form": courseform})


def create_course(request):
    if request.method == "POST":
        course = Course()
        course.title = request.POST.get("title")
        course.description = request.POST.get("description")
        course.save()
    return HttpResponseRedirect("/")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')