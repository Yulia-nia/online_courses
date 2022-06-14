import datetime

from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, response, request
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from rest_framework import generics
from django.urls import reverse, reverse_lazy
from rest_framework.response import Response
from django.views import View
from chat.models import Chat, Message
from course.forms import CourseForm, SettingsForm, CoursEnrollmentForm, CommentForm, NotificationFormCreate
from course.models import Course, Settings, Notifications, РassingРrogress, CoursEnrollment, Comment, RatingScore
from course.serializer import CourseSerializer
from module.forms import AnnouncementForm
from module.models import Announcement, Lesson, Mark, Module, Task, StudentAnswer
from users.models import User, BookmarkCourse
from django.views.generic import TemplateView, ListView, DeleteView
import pandas as pd


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
        return redirect("index")
        # return HttpResponseRedirect("/")
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>Course not found</h2>")


@method_decorator(login_required, name='dispatch')
class CatalogCourses(View):
    def get(self, request):
        courses = Course.objects.all().filter(settings__is_published=True)
        return render(request, "course/course_catalog.html", {"courses": courses})


def view_course(request, id):
    course = Course.objects.get(id=id)
    chat = Chat.objects.all().filter(course_id=course.id)
    user = auth.get_user(request)
    created = BookmarkCourse.objects.all().filter(obj_id=id, user_id=user.id)
    if course.settings.start_date < timezone.now() < course.settings.end_date:
        course.settings.is_active = True
        course.settings.save()
    else:
        course.settings.is_active = False
        course.settings.save()
    is_enrollements = False
    if timezone.now() < course.coursenrollment.time_end:
        is_enrollements = True

    is_student_in_enrollement = False
    if course.coursenrollment.students.all().filter(id=user.id).first():
        is_student_in_enrollement = True

    return render(request, "course/view_course.html", {"course": course, "created": created,
                                                       'is_student_in_enrollement': is_student_in_enrollement,
                                                       'is_enrollements': is_enrollements})


def add_student_in_enrollment(request, id):
    enrollment = Course.objects.get(id=id).coursenrollment
    enrollment.students.add(request.user)
    enrollment.save()
    return HttpResponseRedirect(reverse('view_course', args=(id,)))


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


def get_set_with_value(value):
    if value == '0' or value == '3':
        return False, False
    elif value == '1':
        return True, False
    elif value == '2':
        return True, True


def delete_student_in_enrollment(request, id):
    enrollment = Course.objects.get(id=id).coursenrollment
    user = auth.get_user(request)
    enrollment.students.remove(user)
    enrollment.save()
    return HttpResponseRedirect(reverse('view_course', args=(id,)))


def settings_edit(request, id):
    course = Course.objects.get(id=id)
    setting = Settings.objects.all()
    setting = Settings.objects.filter(course_id=id)
    if setting.count() == 0:
        form = SettingsForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            setting = Settings()
            setting.active_level = form.cleaned_data['active_level']
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

            # setting.is_published, setting.is_active = get_set_with_value(setting.active_level)
            setting.course_id = id
            setting.save()
        return render(request, "course/main_settings.html", {"form": form,
                                                             "course": course,
                                                             "setting": setting,
                                                             "item_id": id})
    else:
        setting = Settings.objects.get(course_id=id)
        form = SettingsForm(request.POST or None, request.FILES or None, initial=
                            { 'active_level': setting.active_level,
                                'learning_format': setting.learning_format,
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
            setting.active_level = form['active_level'].value()
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

            # setting.is_published, setting.is_active = get_set_with_value(setting.active_level)
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
    announcements = Announcement.objects.all().filter(course_id=id).order_by('-id')
    count_list = zip(announcements, range(1, announcements.count()+1))
    course = Course.objects.get(id=id)
    return render(request, "course/announcements/announcement_list.html", {"form_announcement": form_announcement,
                                                             "announcements": announcements,
                                                             "course": course,
                                                             "count_list": count_list,
                                                             "item_id": id})


def create_announcement(request, id):
    course = Course.objects.get(id=id)
    form = AnnouncementForm(request.POST or None)
    if form.is_valid():
        ann = Announcement()
        ann.content = form.cleaned_data['content']
        ann.course_id = id
        ann.save()
        return HttpResponseRedirect(reverse('announcement_list', args=(id,)))
    return render(request, "course/announcements/create_announcement.html", {'course': course,
                                                                           "form": form,
                                                                           })


    if request.method == "POST":
        announcement = Announcement()
        announcement.content = request.POST.get("content")
        announcement.course_id = id
        announcement.save()
    return HttpResponseRedirect(reverse('announcement_list', args=(id,)))


def check_list(request, id):
    course = Course.objects.get(id=id)
    # 1
    desc = course.description.__len__()
    desc_true = True if desc > 100 else False
    # 2
    enrollment = CoursEnrollment.objects.all().filter(course_id=id)
    is_enrollment = False
    enrollment_course = None
    if enrollment.count() != 0:
        is_enrollment =True
        enrollment_course = course.coursenrollment
    # 3 хотябы один
    announcement = Announcement.objects.all().filter(course_id=id).count()
    is_announcement = True if announcement > 0 else False
    # 4 хотябы 2
    modules = Module.objects.all().filter(course_id=id)
    is_module = True if modules.count() > 1 else False
    # 5 хотябы 10 уроков
    lessons = Lesson.objects.all().filter(module__course_id=id)
    is_lesson = True if lessons.count() > 9 else False
    # 6 хотябы 5 открытых уроков
    lessons_open = Lesson.objects.all().filter(module__course_id=id, is_published=True)
    is_lesson_open = True if lessons_open.count() > 4 else False
    # 7 хотябы 5 заданий
    tasks = Task.objects.all().filter(module__course_id=id)
    is_task = True if tasks.count() > 4 else False
    # ----
    # 8 нет пустых модулей
    is_null_modules = True  # нет пустых
    null_modules = []
    for i in modules:
        if i.lesson_set.count() == 0 and i.task_set.count() == 0:
            is_null_modules = False # есть пустой
            null_modules.append(i)
    # 9 нет уроков без блоков
    is_null_lesson = True # нет пустых
    null_lesson = []
    for i in lessons:
        if i.block_set.count() == 0:
            is_null_lesson = False
            null_lesson.append(i)
    # 10 все задания содержат файлы
    is_task_file = True # нет файлов
    tasks_file = []
    for i in tasks:
        if i.file == None:
            is_task_file = False #есть пустой
            tasks_file.append(i)
    count = 0

    is_list = [desc_true, is_enrollment, is_announcement, is_module, is_lesson, is_lesson_open, is_task,
               is_null_lesson, is_null_modules, is_task_file]
    for item in is_list:
        if item:
            count += 1
    progress = count * 10

    return render(request, "course/check_list.html", {"item_id": id,
                                                      'settings': desc,
                                                      'desc_is': desc_true,
                                                      'enrollment_course': enrollment_course,
                                                      'is_enrollment': is_enrollment,
                                                      'announcement': announcement,
                                                      'is_announcement': is_announcement,
                                                      'modules': modules,
                                                      'is_module': is_module,
                                                      'lessons': lessons,
                                                      'is_lesson': is_lesson,
                                                      'lessons_open': lessons_open,
                                                      'is_lesson_open': is_lesson_open,
                                                      'tasks': tasks,
                                                      'is_task': is_task,
                                                      'null_modules': null_modules,
                                                      'is_null_modules': is_null_modules,
                                                      'null_lesson': len(null_lesson),
                                                      'is_null_lesson': is_null_lesson,
                                                      'tasks_file': len(tasks_file),
                                                      'is_task_file': is_task_file,
                                                      'progress': progress,
                                                      "course": course})


def get_student_progress(c_id, s_id):
    return РassingРrogress.objects.all().filter(course_id=c_id, student_id=s_id, is_pass=1).count()


def get_student_answers(c_id, s_id):
    return StudentAnswer.objects.all().filter(student_id=s_id, task__module__course_id=c_id,
                                              mark__isnull=False).count()


def all_for_day(course, time_1):
    pass_lessons = РassingРrogress.objects.all().filter(course_id=course.id, is_pass=True)
    count_lesson = 0
    count_task = 0
    answers = StudentAnswer.objects.all().filter(task__module__course=course)
    for item in pass_lessons:
        if item.time_update.date() == time_1:
            count_lesson += 1
    for item in answers:
        if item.time_create.date() == time_1:
            count_task += 1
    return count_lesson + count_task


def lessons_for_day(course, time_1):
    pass_lessons = РassingРrogress.objects.all().filter(course_id=course.id, is_pass=True)
    count_lesson = 0
    for item in pass_lessons:
        if item.time_update.date() == time_1:
            count_lesson += 1
    return count_lesson


def task_for_day(course, time_1):
    count_task = 0
    answers = StudentAnswer.objects.all().filter(task__module__course=course)
    for item in answers:
        if item.time_create.date() == time_1:
            count_task += 1
    return count_task


def get_statist(course):
    d_pie = pd.date_range(end=datetime.date.today(), periods=7)
    date_pie = [str(i.date()) for i in d_pie]
    data_pie_all = []
    data_pie_task = []
    data_pie_lesson = []
    for item in d_pie:
        data_pie_all.append(all_for_day(course, item.date()))
        data_pie_task.append((task_for_day(course, item.date())))
        data_pie_lesson.append((lessons_for_day(course, item.date())))
    return date_pie, data_pie_all, data_pie_task, data_pie_lesson


def get_students_done(course, task_count, lesson_count):
    students = course.coursenrollment.students.all()
    students_pass = []
    students_done = []
    for i in students:
        c = 0
        answer = StudentAnswer.objects.all().filter(task__module__course=course, mark__isnull=False,
                                                    student_id=i.id)
        if task_count == answer.count():
            c += 1
        pass_lessons = РassingРrogress.objects.all().filter(is_pass=True, course_id=course.id,
                                                            student_id=i.id)
        if lesson_count == pass_lessons.count():
            c += 1
        if c == 2:
            students_done.append(i)
        else:
            students_pass.append(i)
    return students_pass, students_done


class StudentList(View):

    def get(self, request, id):
        course = Course.objects.get(id=id)
        lesson = Lesson.objects.all().filter(module__course_id=id)
        tasks = Task.objects.all().filter(module__course_id=id)
        students = []
        progress = []
        answers = []
        for i in course.coursenrollment.students.all():
            students.append(i)
            progress.append(get_student_progress(course.id, i.id))
            answers.append(get_student_answers(course.id, i.id))
        count_lessons = lesson.count()

        date_pie, data_pie_all, data_pie_task, data_pie_lesson = get_statist(course)

        labels = []
        data = []
        students_pass_course, students_done_course = get_students_done(course, tasks.count(), count_lessons)
        labels.append('В процессе')
        data.append(len(students_pass_course))
        labels.append('Завершили курс')
        data.append(len(students_done_course))

        # for item in range(1, len(d_p)):
        #     data_pie.append(task_lessons_for_day(course, d_p[item - 1], d_p[item]))

        # student_answers = StudentAnswer.objects.all().filter(student_id=user.id, task__module__course_id=course.id)

        return render(request, "course/students_list.html", {"item_id": id,
                                                             "count_lessons": count_lessons,
                                                             'count_task': tasks.count(),
                                                             "list_item": zip(students, progress, answers),
                                                             "course": course,
                                                             'date_pie':date_pie,
                                                             'data_pie_all': data_pie_all,
                                                             'data_pie_task': data_pie_task,
                                                             'labels': labels,
                                                             'data': data,
                                                             'data_done': data[1],
                                                             'data_pass': data[0],
                                                             'students_done_course': students_done_course,
                                                             'data_pie_lesson': data_pie_lesson,

                                                             "form": NotificationFormCreate(),
                                                             })
    def post(self, request, id):
        course = Course.objects.get(id=id)
        lesson = Lesson.objects.all().filter(module__course_id=id)
        students = []
        progress = []
        answers = []
        for i in course.coursenrollment.students.all().order_by('-id'):
            students.append(i)
            progress.append(get_student_progress(course.id, i.id))
            answers.append(get_student_answers(course.id, i.id))
        count_lessons = lesson.count()
        if request.method == 'POST':
            form = NotificationFormCreate(request.POST)
            course = get_object_or_404(Course, id=id)
            if form.is_valid():
                form = form.save(commit=False)
                if request.POST.get("student_id", None):
                    form.student_id = int(request.POST.get("student_id"))
                form.course = course
                form.save()
            return HttpResponseRedirect(reverse('students_list', args=(id,)))
            # return render(request, "course/students_list.html", {"course": Course.objects.get(id=id),
            #                                                              "item_id": id,
            #                                                              "count_lessons": count_lessons,
            #                                                              'form': form,
            #                                                              "list_item": zip(students, progress, answers),
            #                                                              })

        #
        # if request.method == "POST":
        #     notification = Notifications()
        #     notification.content = request.POST.get("content")
        #     notification.course_id = id
        #     notification.student_id = s_id
        #     notification.save()
        #     return HttpResponseRedirect(reverse('students_list', args=(id,)))
        # else:
        #     return render(request, "course/notifications/create_notification.html",
        #                   {"course": Course.objects.get(id=id),
        #                    "student": User.objects.get(id=s_id),
        #                    "form": NotificationForm(),
        #                    })


#
# def students_list(request, id):
#     course = Course.objects.get(id=id)
#
#     lesson = Lesson.objects.all().filter(module__course_id=id)
#     students = []
#     progress = []
#     for i in course.coursenrollment.students.all().order_by('-id'):
#         students.append(i)
#         progress.append(get_student_progress(course.id, i.id))
#
#     count_lessons = lesson.count()
#     return render(request, "course/students_list.html", {"item_id": id,
#                                                          "count_lessons": count_lessons,
#                                                          "list_item": zip(students, progress),
#                                                          "course": course,
#                                                          "form": NotificationForm(),
#                                                          })

#
#
# def create_notification(request, id, s_id):
#     if request.method == "POST":
#         notification = Notifications()
#         notification.content = request.POST.get("content")
#         notification.course_id = id
#         notification.student_id = s_id
#         notification.save()
#         return HttpResponseRedirect(reverse('students_list', args=(id,)))
#     else:
#         return render(request, "course/notifications/create_notification.html",
#                   {"course": Course.objects.get(id=id),
#                    "student": User.objects.get(id=s_id),
#                    "form": NotificationForm(),
#                    })


class CourseAPIView(generics.ListAPIView):
    # queryset = Course.objects.all()
    # serializer_class = CourseSerializer

    def get(self, request):
        course = Course.objects.all()
        return Response({'courses': CourseSerializer(course, many=True).data})


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

def all_noti_day(course, time_1):
    count_nottif = 0
    noti = []
    answers = Notifications.objects.all().filter(course_id=course.id)
    for item in answers:
        if item.time_create.date() == time_1:
            count_nottif += 1
            noti.append(item)
    return count_nottif, noti


def get_statist_notif(course):
    d_pie = pd.date_range(end=datetime.date.today(), periods=10)
    date_pie = [str(i.date()) for i in d_pie]
    data_pie_all = []
    arr_noti = []
    for item in d_pie:
        int_count, arr = all_noti_day(course, item.date())
        data_pie_all.append(int_count)
        arr_noti.append(arr)
    return date_pie, data_pie_all, arr_noti


def notifications_list_course(request, id):
    course = Course.objects.get(id=id)
    notifications = Notifications.objects.all().filter(course_id=id)

    students = []
    users = BookmarkCourse.objects.all().filter(obj_id=id)
    for i in users:
        students.append(User.objects.get(id=i.user_id))

    user = auth.get_user(request)
    s_notifications = Notifications.objects.all().filter(course_id=id, student_id=user.id)

    date_pie, data_pie_all, arr_noti = get_statist_notif(course)
    z = zip(date_pie, arr_noti)

    return render(request, "course/notifications/notifications_list.html", {"course": course,
                                                         "students": students,
                                                         "notifications": notifications,
                                                                      'labels':date_pie,
                                                                       'data': data_pie_all,
                                                                            'z': z,
                                                                            'arr_noti': arr_noti,

                                                        "s_notifications": s_notifications,})


def grades_list(request, id):
    course = Course.objects.get(id=id)

    students_list = User.objects.all().filter(ratingscore__course_id=id)



    marks = Mark.objects.all().filter(course_id=id)

    rating = RatingScore.objects.all().filter(course_id=id)
    modules = Module.objects.all().filter(course_id=id)

    count_all = Task.objects.all().filter(module__course_id=id).count()

    return render(request, "module/mark/grades_list.html",
                  {"course": course,
                   'students': students_list,
                   "rating": rating,
                   "marks": marks,
                   "count_all": count_all,
                   "modules": modules,
                   "sr_mark": 6,
                   })


def edit_announcements(request, id):
    ann = Announcement.objects.get(id=id)
    form = AnnouncementForm(request.POST or None, initial=
    {'content': ann.content})
    if form.is_valid():
        ann.content = form['content'].value()
        ann.course_id = ann.course_id
        ann.save()
        return HttpResponseRedirect(reverse('announcement_list', args=(ann.course_id,)))
    return render(request, "course/announcements/edit_announcement.html", {'course': ann.course,
                                                     "form": form,
                                                     "ann": ann})


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


class EnrollmentView(View):
    model = CoursEnrollment

    def get(self, request, id):
        course = Course.objects.get(id=id)
        enrollments = CoursEnrollment.objects.all().filter(course_id=id).first()
        form = CoursEnrollmentForm()
        return render(request, "course/enrollments/list.html", {"course": course,
                                                                'enrollments': enrollments if enrollments else None,
                                                                'form': form})

    def post(self, request, id):
        course = Course.objects.get(id=id)
        enrollment_edit = CoursEnrollment.objects.all().filter(course_id=id)
        if enrollment_edit.count() == 1:
            enrollment_edit = enrollment_edit.first()
            form = CoursEnrollmentForm(request.POST or None, initial={'time_end': enrollment_edit.time_end,
                                                                      'time_create': enrollment_edit.time_create})
            if form.is_valid():
                #enrollment_edit.time_create = DateTimePickerInput()
                enrollment_edit.time_create = form['time_create'].value()
                enrollment_edit.time_end = form['time_end'].value()
                enrollment_edit.course_id = id
                enrollment_edit.save()
        else:
            enrollment = CoursEnrollment()


            form = CoursEnrollmentForm(request.POST)
            if form.is_valid():
                enrollment_edit.time_create = form.cleaned_data['time_create']
                enrollment.time_end = form.cleaned_data['time_end']
                enrollment.course_id = id
                enrollment.save()
        enrollments = CoursEnrollment.objects.get(course_id=id)
        return render(request, "course/enrollments/list.html", {"course": course,
                                                                'enrollments': enrollments,
                                                                'form': form})


from django.template.context_processors import csrf


class CommentView(View):
    template_name = 'course/comment/list_comments.html'
    comment_form = CommentForm

    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        context = {}
        context.update(csrf(request))
        user = auth.get_user(request)
        commnets = course.comment_set.all().order_by('-id')
        if user.is_authenticated:
            form = self.comment_form
            return render(request, "course/comment/list_comments.html", {"course": course,
                                                                         'commnets': Course.objects.get(id=id).comment_set.all().filter(parent_id=None),
                                                                         'form': form})

        return render(request, "course/comment/list_comments.html", {"course": course,
                                                                     'commnets': Course.objects.get(id=id).comment_set.all().filter(parent_id=None),
                                                                     'form': self.comment_form,
                                                                     })

    def post(self, request, id):
        if request.method == 'POST':
            form = CommentForm(request.POST)
            course = get_object_or_404(Course, id=id)
            if form.is_valid():
                form = form.save(commit=False)
                if request.POST.get("parent", None):
                    form.parent_id = int(request.POST.get("parent"))
                form.course = course
                form.author = auth.get_user(request)
                form.save()
            return render(request, "course/comment/list_comments.html", {"course": Course.objects.get(id=id),
                                                                  'commnets': Course.objects.get(id=id).comment_set.all().filter(parent_id=None),
                                                                  'form': form
                                                                 })
