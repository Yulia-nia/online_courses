from django.contrib import auth
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, response
from django.utils.timezone import now
from rest_framework import generics
# Create your views here.
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response

from chat.models import Chat, Message
from course.forms import CourseForm, SettingsForm
from course.models import Course, Settings
from course.serializer import CourseSerializer
from module.forms import AnnouncementForm
from module.models import Announcement
from users.models import User, BookmarkCourse


def index(request):
    courseform = CourseForm()
    user = User.objects.get(username=request.user.username)
    courses = Course.objects.all().filter(author_id=user.id)
    return render(request, "course/index.html", {"form": courseform, "courses": courses})


def catalog_courses(request):
    courses = Course.objects.all()
    return render(request, "course/course_catalog.html", {"courses": courses})


def view_course(request, id):
    course = Course.objects.get(id=id)
    user = auth.get_user(request)
    bookmark, created = BookmarkCourse.objects.get_or_create(user=user, obj_id=id)
    # если не была создана новая закладка,
    # то считаем, что запрос был на удаление закладки
    chat = Chat.objects.all().filter(course_id=course.id)
    if not created:
        bookmark.delete()
    return render(request, "course/view_course.html", {"course": course})


def pass_course(request, id):
    course = Course.objects.get(id=id)
    return render(request, "course/pass_course.html", {"course": course})


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

            setting.will_learn = form.cleaned_data["will_learn"]
            setting.about_course = form.cleaned_data["about_course"]
            setting.necessary_training = form.cleaned_data["necessary_training"]
            setting.how_training = form.cleaned_data["how_training"]
            setting.what_you_get = form.cleaned_data["what_you_get"]
            setting.level = form.cleaned_data["level"]

            setting.course_id = id
            setting.save()
        return render(request, "course/main_settings.html", {"form": form, "setting": setting, "item_id": id})
    else:
        setting = Settings.objects.get(course_id=id)
        form = SettingsForm(request.POST or None, request.FILES or None, initial=
                            { 'learning_format': setting.learning_format,
                              'subject': setting.subject,
                                      'language': setting.language,
                                      'image': setting.image,
                                      'is_published': setting.is_published,
                                      'course_id': setting.course_id,
                              'will_learn': setting.will_learn,
                              'about_course': setting.about_course,
                              'necessary_training': setting.necessary_training,
                              'how_training': setting.how_training,
                              'what_you_get': setting.what_you_get,
                              'level': setting.level,
                              }
                            )
        if form.is_valid():
            setting.learning_format = form['learning_format'].value()
            setting.subject = form["subject"].value()
            setting.language = form['language'].value()
            setting.image = form["image"].value()
            setting.is_published = form["is_published"].value()

            setting.will_learn = form["will_learn"].value()
            setting.about_course = form["about_course"].value()
            setting.necessary_training = form["necessary_training"].value()
            setting.how_training = form["how_training"].value()
            setting.what_you_get = form["what_you_get"].value()
            setting.level = form["level"].value()

            setting.course_id = id
            setting.save()
        return render(request, "course/main_settings.html", {"form": form, "setting": setting, "item_id": id})


def create_course(request):
    if request.method == "POST":
        course = Course()
        course.title = request.POST.get("title")
        course.description = request.POST.get("description")
        course.author = User.objects.get(username=request.user.username)
        course.save()
    return HttpResponseRedirect("/")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def edit_course(request, id):
    course = Course.objects.get(id=id)
    form = CourseForm(request.POST or None, initial=
        {'title': course.title, 'description': course.description})
    if form.is_valid():
        course.title = form['title'].value()
        course.description = form["description"].value()

        course.save()
    return render(request, "course/edit_course.html", {"course": course, 'form': form, "item_id": id})


def delete_course(request, id):
    try:
        course = Course.objects.get(id=id)
        course.delete()
        return HttpResponseRedirect("/")
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>Course not found</h2>")


def announcement_list(request, id):
    form_announcement = AnnouncementForm()
    announcements = Announcement.objects.all().filter(course_id=id)
    count_list = zip(announcements, range(1, announcements.count()+1))
    return render(request, "course/announcement_list.html", {"form_announcement": form_announcement,
                                                             "announcements": announcements,
                                                             "count_list": count_list,
                                                             "item_id": id})


def create_announcement(request, id):
    if request.method == "POST":
        announcement = Announcement()
        announcement.content = request.POST.get("content")
        announcement.course_id = id
        announcement.save()
    return HttpResponseRedirect(reverse('announcement_list', args=(id,)))


def check_list(request, id):
    return render(request, "course/check_list.html", {"item_id": id})


def students_list(request, id):
    course = Course.objects.get(id=id)
    students = []
    users = BookmarkCourse.objects.all().filter(obj_id=id)
    for i in users:
        students.append(User.objects.get(id=i.user_id))
    return render(request, "course/students_list.html", {"item_id": id, "students": students})


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


def dialog(request, c_id):
    course = Course.objects.get(id=c_id)
    if course.chat_set.count() == 0:
        chat = Chat.objects.create(
            course_id=course.id
        )
        chat.members.add(request.user)
        chat.members.add(course.author_id)
        message = Message.objects.create(chat_id=chat.id,
                                         message='Добро пожаловать в чат',
                                         author_id=course.author_id,
                                         )
        chat.save()
        message.save()
        return render(request, "../../chat/templates/chat/dialogs.html", {"course_id": c_id,
                                                                          "chat": chat,
                                                                            "chat_id": chat.id, "instructor": course.author})
    else:
        chat = Chat.objects.get(course_id=course.id)
        chat.members.add(request.user)
        chat.save()
        return render(request, "../../chat/templates/chat/dialogs.html", {"course_id": c_id,
                                                            "chat": chat,
                                                            "chat_id": chat.id, "instructor": course.author})
