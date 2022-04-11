from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from rest_framework import generics
# Create your views here.
from django.urls import reverse
from rest_framework.response import Response

from course.forms import CourseForm
from course.models import Course, Settings
from course.serializer import CourseSerializer


def index(request):
    courseform = CourseForm()
    courses = Course.objects.all()
    return render(request, "course/index.html", {"form": courseform, "courses": courses})


def settings_edit(request, id):
    setting = Settings.objects.all()
    setting = Settings.objects.filter(course_id=id)
    if setting.count() == 0:
        if request.method == "POST":
             setting = Settings()
             setting.learning_format = request.POST.get("learning_format")
             setting.subject = request.POST.get("subject")
             setting.language = request.POST.get("language")
             setting.course_id = id
             setting.save()
        return render(request, "course/main_settings.html", {"setting": setting, "item_id": id})
    else:
        setting = Settings.objects.get(course_id=id)
        if request.method == "POST":
            setting.learning_format = request.POST.get("learning_format")
            setting.subject = request.POST.get("subject")
            setting.language = request.POST.get("language")
            setting.save()
        return render(request, "course/main_settings.html", {"setting": setting, "item_id": id})


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


class CourseAPIView(generics.ListAPIView):
    # queryset = Course.objects.all()
    # serializer_class = CourseSerializer

    def get(self, request):
        course = Course.objects.all()
        return Response({'courses': CourseSerializer(course, many=True).data})

    # def post(self, request):
    #     serializer = CourseSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response({'course': serializer.data})
    #
    # # update
    # def put(self, request, *args, **kwargs):
    #     pk = kwargs.get("pk", None)
    #     if not pk:
    #         return Response({"error": "Method PUT not allowed"})
    #     try:
    #         instance = Course.objects.get(pk=pk)
    #     except:
    #         return Response({"error": "Object does not exists"})
    #     serializer = CourseSerializer(data=request.data, instance=instance)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response({"course": serializer.data})

