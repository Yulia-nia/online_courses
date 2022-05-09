from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse
# Create your views here.
from django.views import View

from course.models import Course, РassingРrogress
from module.forms import ModuleForm, AnnouncementForm, LessonEditForm, TaskForm, AnswerTaskForm, MarkForm
from module.models import Module, Lesson, Announcement, File, Task, StudentAnswer, Mark
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from jinja2 import Environment


def list_module(request, id):
    course = Course.objects.get(id=id)
    form = ModuleForm()
    modules = Module.objects.all()
    #form_announcement = AnnouncementForm()

    #announcements = Announcement.objects.all().filter(course_id=id)

    #count_list = zip(announcements, range(1, announcements.count()+1))
    # in case to filter by id

    #pass_prog = РassingРrogress.objects.get(course_id=id, student_id=request.user.id)

    modules = Module.objects.filter(course_id=id)
    lessons = Lesson.objects.all().filter(module__course_id=id)

    student_progress = РassingРrogress.objects.all().filter(course_id=id, student_id=request.user.id ,is_pass=1).count()
    count_lessons = lessons.count()

    return render(request, "module/module_list.html", {"form": form, "modules": modules,
                                                       # "form_announcement": form_announcement,
                                                       # "announcements": announcements,
                                                       # "lesson": lesson,
                                                        "count_lessons":count_lessons,
                                                       "student_progress":student_progress,
                                                       "course": course,
                                                       "lessons": lessons,
                                                       "item_id": id})


def get_lessons(id):
    lessons = Lesson.objects.all().filter(module_id=id)
    arr = [i for i in lessons]
    env = Environment(id)
    env.globals.update({
        'lessons': arr,
    })
    return env


def create_module(request, id):
    if request.method == "POST":
        module = Module()
        module.title = request.POST.get("title")
        module.course_id = id
        module.save()
    return HttpResponseRedirect(reverse('list', args=(id,)))


def create_lesson(request, m_id, id):
    module = Module.objects.get(id=m_id)
    course = Course.objects.get(id=module.course_id)
    lesson = Lesson()
    if request.method == "POST":
        lesson.title = request.POST.get("title")
        lesson.short_description = request.POST.get("short_description")
        lesson.description = request.POST.get("description")
        lesson.module_id = m_id
        lesson.save()
    return render(request, "module/create_lesson.html", {"lesson": lesson,
                                                         "course": course,
                                                         "item_id": m_id,
                                                         })


def create_task(request, id):
    module = Module.objects.get(id=id)
    course = Course.objects.get(id=module.course_id)
    if request.method == "POST":
        form = TaskForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            task = Task()
            task.title = form.cleaned_data['title']
            task.description = form.cleaned_data["description"]
            task.file = form.cleaned_data['file']
            task.time_deadline = form.cleaned_data['time_deadline']
            task.module_id = id
            task.save()
        return HttpResponseRedirect(reverse('list', args=(course.id,)))
    else:
        return render(request, "module/task/create.html",
                      {"module": module,
                       "course": course,
                       "form": TaskForm()})


def list_answers_tasks(request, id):
    list_module = Module.objects.all().filter(course_id=id)
    return render(request, "module/task/list_answer.html", {
                                                            "list_module": list_module,
                                                       "course": Course.objects.get(id=id),})


def list_ans_from_task(request, id):
    answers = StudentAnswer.objects.all().filter(task_id=id)
    task = Task.objects.get(id=id)
    module = Module.objects.get(id= task.module_id)
    return render(request, "module/task/list_answer_from_task.html", {
        "answers": answers,
        "course": Course.objects.get(id=module.course_id) })



def edit_lesson(request, id):
    try:
        lesson = Lesson.objects.get(id=id)
        module = Module.objects.get(id=lesson.module_id)
        course = Course.objects.get(id=module.course_id)
        form = LessonEditForm(request.POST or None, request.FILES or None, initial=
                                    {'title': lesson.title,
                                     'description': lesson.description,
                                     'short_description': lesson.short_description,
                                     'is_published': lesson.is_published,
                                     })
        files = File.objects.all().filter(lesson_id=lesson.id)
        if form.is_valid():
            lesson.title = form['title'].value()
            lesson.description = form["description"].value()
            lesson.short_description = form['short_description'].value()
            lesson.is_published = form['is_published'].value()
            lesson.save()
            return render(request, "module/edit_lesson.html", {"lesson": lesson,
                                                               "item_id": module.course_id,
                                                               "form": form,
                                                               "course": course,
                                                               "files": files})
        else:
            return render(request, "module/edit_lesson.html", {"lesson": lesson,
                                                               "item_id": module.course_id,
                                                               "course": course,
                                                               "form": form, "files": files})
    except Lesson.DoesNotExist:
        return HttpResponseNotFound("<h2>Lesson not found</h2>")


def view_lesson(request, id):
    try:
        lesson = Lesson.objects.get(id=id)
        module = Module.objects.get(id=lesson.module_id)
        course = Course.objects.get(id=module.course_id)
        files = File.objects.all().filter(lesson_id=lesson.id)
        progress_is = get_progress(course.id, lesson.id, request.user.id)
        return render(request, "module/view_lesson.html", {"lesson": lesson,
                                                           "module": module,
                                                           "course": course,
                                                            "files": files,
                                                           "progress_is": progress_is})
    except Lesson.DoesNotExist:
        return HttpResponseNotFound("<h2>Lesson not found</h2>")



def edit_module(request, id):
    try:
        module = Module.objects.get(id=id)
        course = Course.objects.get(id=module.course_id)
        lessons = Lesson.objects.all().filter(module_id=id)
        return render(request, "module/edit_module.html", {"module": module,
                                                           "course": course,
                                                           "lessons": lessons,
                                                           "module_id": id})
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


def delete_module(request, id):
    try:
        module = Module.objects.get(id=id)
        id_course = module.course_id
        module.delete()
        return HttpResponseRedirect(reverse('list', args=(id_course,)))
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>Module not found</h2>")


def get_progress(c_id, l_id, u_id):
    progress_is, obj = РassingРrogress.objects.get_or_create(lesson_id=l_id,
                                                             course_id=c_id,
                                                             student_id=u_id)
    return progress_is


def progress(request, id):
    lesson = Lesson.objects.get(id=id)
    module = Module.objects.get(id=lesson.module_id)
    files = File.objects.all().filter(lesson_id=lesson.id)
    course = Course.objects.get(id=lesson.module.course_id)
    progress_is = get_progress(course.id, lesson.id, request.user.id)
    if progress_is.is_pass == 1:
        progress_is.is_pass = 0
    else:
        progress_is.is_pass = 1
    progress_is.save()
    return HttpResponse()
    #return request.META.get('view_lesson')
    # return HttpResponse('view_lesson', args=(lesson, module,
    #                                                  course,
    #                                                          course.id,
    #                                                     list(files),
    #                                                     progress_is,))
    # render(request, "module/view_lesson.html", {"lesson": lesson,
    #                                                        "module": module,
    #                                                        "course": course,
    #                                                         "files": files,
    #                                                        "progress_is": progress_is})



class TaskView(View):
    def get(self, request, id):
        try:
            task = Task.objects.get(id=id)
            course = Course.objects.get(id=task.module.course_id)
            answer = StudentAnswer.objects.all().filter(student_id=request.user.id,
                                                        task_id=id)
            return render(
            request,
            "module/task/view_task.html", {"course": course, "task": task,
                                           "answer": answer,
                                           'form': AnswerTaskForm()
                                           })
        except Task.DoesNotExist:
            task = None
            course = None
            answer = None
        return render(
            request,
            "module/task/view_task.html", {"course": course, "task": task,
                                           'answer': answer,
                                           'form': AnswerTaskForm()
                                           })

    def post(self, request, id):
        task = Task.objects.get(id=id)
        course = Course.objects.get(id=task.module.course_id)

        form = AnswerTaskForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            answer = StudentAnswer()
            answer.description = form.cleaned_data["description"]
            answer.file = form.cleaned_data['file']
            answer.task_id = id
            answer.student_id = request.user.id
            answer.save()
        return render(request, "module/task/view_task.html", {'course': course,
                                                      "form": AnswerTaskForm(),
                                                      "task": task})


class EstimateView(View):
    def get(self, request, id):
        try:
            answer = StudentAnswer.objects.get(id=id)
            task = answer.task
            course = answer.task.module.course
            return render(
                request,
                "module/task/estimate_answer.html", {"course": course, "task": task,
                                                     "answer": answer,
                                                     'form': MarkForm()
                                                     })
        except Task.DoesNotExist:
            task = None
            course = None
            answer = None
        return render(
            request,
            "module/task/estimate_answer.html", {"course": course, "task": task,
                                           'answer': answer,
                                           'form': MarkForm()
                                           })

    def post(self, request, id):
        answer = StudentAnswer.objects.get(id=id)
        task = answer.task
        course = answer.task.module.course
        form = MarkForm(request.POST or None)
        if form.is_valid():
            mark = Mark()
            mark.mark = form.cleaned_data["mark"]
            mark.answer_id = answer.id
            mark.course_id = course.id
            mark.student_id = answer.student_id
            mark.save()
        return render(request, "module/task/estimate_answer.html", {'course': course,
                                                              "form": MarkForm(),
                                                              "task": task,
                                                              })


def edit_task(request, id):
    task = Task.objects.get(id=id)
    form = TaskForm(request.POST or None, request.FILES or None, initial=
                    {'title': task.title,
                     'description': task.description,
                     'time_deadline': task.time_deadline,
                     'file': task.file,})
    if form.is_valid():
        task.title = form['title'].value()
        task.description = form["description"].value()
        task.time_deadline = form['time_deadline'].value()
        task.file = form["file"].value()
        task.module_id = task.module_id
        task.save()
    return render(request, "module/task/edit.html", {'course': task.module.course,
                                                          "form": form,
                                                          "task": task})


def delete_task(request, id):
    try:
        task = Task.objects.get(id=id)
        id_course = task.module.course.id
        task.delete()
        return HttpResponseRedirect(reverse('list', args=(id_course,)))
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>task not found</h2>")


def content_course(request, id):
    course = Course.objects.get(id=id)
    modules = Module.objects.all().filter(course_id=id)
    return render(request, "module/content/base_nav.html", {'course': course,

                                                          "modules": modules,
                                                          })

