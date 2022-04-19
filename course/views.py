from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, response
from rest_framework import generics
# Create your views here.
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response

from course.forms import CourseForm, SettingsForm
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
        form = SettingsForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            setting = Settings()
            setting.learning_format = form.cleaned_data['learning_format']
            setting.subject = form.cleaned_data["subject"]
            setting.language = form.cleaned_data['language']
            setting.image = form.cleaned_data["image"]
            setting.is_published = form.cleaned_data["is_published"]
            setting.course_id = id
            setting.save()
        return render(request, "course/main_settings.html", {"form": form, "item_id": id})
    else:
        setting = Settings.objects.get(course_id=id)
        form = SettingsForm(request.POST or None, request.FILES or None, initial=
                            { 'learning_format': setting.learning_format,
                              'subject': setting.subject,
                                      'language': setting.language,
                                      'image': setting.image,
                                      'is_published': setting.is_published,
                                      'course_id': setting.course_id,}
                            )
        if form.is_valid():
            setting.learning_format = form['learning_format'].value()
            setting.subject = form["subject"].value()
            setting.language = form['language'].value()
            setting.image = form["image"].value()
            setting.is_published = form["is_published"].value()
            setting.course_id = id
            setting.save()

        # setting = Settings.objects.get(course_id=id)
        # if (request.method == "POST" or None) and (request.FILES or None):
        #     setting.learning_format = request.POST.get("learning_format")
        #     setting.subject = request.POST.get("subject")
        #     setting.language = request.POST.get("language")
        #
        #     # if request.FILES.get("image"):
        #     #     setting.image = request.FILES.get("image")
        #     # else:
        #     #     setting.image = 'settings.MEDIA_ROOT/course_img/blog_1.jpg'
        #     if request.FILES.get("image"):
        #         setting.image = request.FILES.get('image')
        #     else:
        #         setting.image = request.FILES.get('image1')
        #
        #     if request.POST.get("player_check") == 'on':
        #         setting.is_published = True
        #     else:
        #         setting.is_published = False
        #     setting.save()
        return render(request, "course/main_settings.html", {"form": form, "item_id": id})


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

