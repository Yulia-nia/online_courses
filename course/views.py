from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, response, request
from django.utils.decorators import method_decorator
from rest_framework import generics
from django.urls import reverse, reverse_lazy
from rest_framework.response import Response
from django.views import View
from chat.models import Chat, Message
from course.forms import CourseForm, SettingsForm, NotificationForm
from course.models import Course, Settings, Notifications, РassingРrogress
from course.serializer import CourseSerializer
from module.forms import AnnouncementForm
from module.models import Announcement, Lesson, Mark, Module
from users.models import User, BookmarkCourse
from django.views.generic import TemplateView, ListView, DeleteView


@method_decorator(login_required, name='dispatch')
class СoursesРarticularTeacher(ListView):
    context_object_name = 'courses'
    queryset = Course.objects.all()
    template_name = 'course/index.html'

    def get(self, request):
        courses = Course.objects.all().filter(author_id=request.user.id)
        return render(request, "course/index.html", {"courses": courses, 'form': CourseForm()})

    def post(self, request):
        courses = Course.objects.all().filter(author_id=request.user.id)
        course = Course()
        course.title = request.POST.get("title")
        course.description = request.POST.get("description")
        course.author = User.objects.get(username=request.user.username)
        course.save()
        return render(request, "course/index.html", {"courses": courses, 'form': CourseForm()})


def delete_course(request, id):
    try:
        course = Course.objects.get(id=id)
        course.delete()
        return HttpResponseRedirect("/")
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>Course not found</h2>")


@method_decorator(login_required, name='dispatch')
class CatalogCourses(View):
    def get(self, request):
        courses = Course.objects.all().filter(settings__is_published=True)
        return render(request, "course/course_catalog.html", {"courses": courses})


def view_course(request, id):
    course = Course.objects.get(id=id)
    user = auth.get_user(request)

    # если не была создана новая закладка,
    # то считаем, что запрос был на удаление закладки
    chat = Chat.objects.all().filter(course_id=course.id)
    user = auth.get_user(request)
    created = BookmarkCourse.objects.all().filter(obj_id=id, user_id=user.id)
    return render(request, "course/view_course.html", {"course": course, "created": created})


def pass_course(request, id):
    course = Course.objects.get(id=id)
    user = auth.get_user(request)
    bookmark, created = BookmarkCourse.objects.get_or_create(user=user, obj_id=id)
    if not created:
        bookmark.delete()
    return render(request, "course/pass_course/pass_course.html", {"course": course})




def info_course(request, id):
    course = Course.objects.get(id=id)
    setting = Settings.objects.get_or_create(course_id=id)
    instructor = course.author
    return render(request, "course/pass_course/info_course.html", {"course": course,
                                                                   "instructor": instructor,
                                                                   "setting": setting })


def settings_edit(request, id):
    course = Course.objects.get(id=id)
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
        return render(request, "course/main_settings.html", {"form": form,
                                                             "course": course,
                                                             "setting": setting,
                                                             "item_id": id})
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
        return render(request, "course/main_settings.html", {"form": form,
                                                             "course": course,
                                                             "setting": setting,
                                                             "item_id": id})


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


def announcement_list(request, id):
    form_announcement = AnnouncementForm()
    announcements = Announcement.objects.all().filter(course_id=id)
    count_list = zip(announcements, range(1, announcements.count()+1))
    course = Course.objects.get(id=id)
    return render(request, "course/announcements/announcement_list.html", {"form_announcement": form_announcement,
                                                             "announcements": announcements,
                                                             "course": course,
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
    course = Course.objects.get(id=id)
    return render(request, "course/check_list.html", {"item_id": id,
                                                      "course": course})

def get_student_progress(c_id, s_id):
    return РassingРrogress.objects.all().filter(course_id=c_id, student_id=s_id, is_pass=1).count()


def students_list(request, id):
    course = Course.objects.get(id=id)
    lesson = Lesson.objects.all().filter(module__course_id=id)
    students = []
    progress = []
    users = BookmarkCourse.objects.all().filter(obj_id=id)
    for i in users:
        students.append(User.objects.get(id=i.user_id))
        progress.append(get_student_progress(course.id, i.user_id))

    count_lessons = lesson.count()
    return render(request, "course/students_list.html", {"item_id": id,
                                                         "count_lessons": count_lessons,
                                                         "list_item": zip(students, progress),
                                                         "course": course,
                                                         })


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
                                                                          "course": course,
                                                                        "chat_id": chat.id,
                                                                          "instructor": course.author})
    else:
        chat = Chat.objects.get(course_id=course.id)
        chat.members.add(request.user)
        chat.save()
        return render(request, "../../chat/templates/chat/dialogs.html", {"course_id": c_id,
                                                                        "chat": chat,
                                                                        "course": course,
                                                                        "chat_id": chat.id,
                                                                        "instructor": course.author})


# def progress(request, lesson_id):
#
#
#     return None


def notifications_list_course(request, id):
    course = Course.objects.get(id=id)
    notifications = Notifications.objects.all().filter(course_id=id)

    students = []
    users = BookmarkCourse.objects.all().filter(obj_id=id)
    for i in users:
        students.append(User.objects.get(id=i.user_id))

    user = auth.get_user(request)
    s_notifications = Notifications.objects.all().filter(course_id=id, student_id=user.id)

    return render(request, "course/notifications/notifications_list.html", {"course": course,
                                                         "students": students,
                                                         "form": NotificationForm(),
                                                         "notifications": notifications,
                                                        "s_notifications": s_notifications,})


def create_notification(request, id, s_id):
    if request.method == "POST":
        notification = Notifications()
        notification.content = request.POST.get("content")
        notification.course_id = id
        notification.student_id = s_id
        notification.save()
        return HttpResponseRedirect(reverse('students_list', args=(id,)))
    else:
        return render(request, "course/notifications/create_notification.html",
                  {"course": Course.objects.get(id=id),
                   "form": NotificationForm(),
                   })


def grades_list(request, id):
    course = Course.objects.get(id=id)
    marks = Mark.objects.all().filter(course_id=id)
    modules = Module.objects.all().filter(course_id=id)
    return render(request, "module/mark/grades_list.html",
                  {"course": course,
                   "marks": marks,
                   "modules": modules,
                   })


def edit_announcements(request, id):
    ann = Announcement.objects.get(id=id)
    form = AnnouncementForm(request.POST or None, initial=
    {'content': ann.content})
    if form.is_valid():
        ann.content = form['content'].value()
        ann.course_id = ann.course_id
        ann.save()
    return render(request, "course/announcements/edit_announcement.html", {'course': ann.course,
                                                     "form": form,
                                                     "task": ann})

    return None


def delete_announcements(request, id):
    try:
        ann = Announcement.objects.get(id=id)
        id_course = ann.course_id
        ann.delete()
        return HttpResponseRedirect(reverse('announcement_list', args=(id_course,)))
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>task not found</h2>")


def student_notifications_list(request):
    studnet = User.objects.get(id=request.user.id)
    notifications = Notifications.objects.all().filter(student_id=studnet.id)
    return render(request, "course/notifications/student_list.html", {'notifications': notifications,})


