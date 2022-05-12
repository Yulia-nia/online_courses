
from django.contrib import messages
from django.db import IntegrityError, transaction

from datetime import datetime
from time import strftime, gmtime

from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse
# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from course.models import Course, РassingРrogress
from module.forms import ModuleForm, AnnouncementForm, LessonEditForm, TaskForm, AnswerTaskForm, MarkForm, \
    LessonCreateForm, BlockCreateForm, BlockForm, BaseLinkFormSet, FileForm, UrlLinkForm, BaseFileFormSet
from module.models import Module, Lesson, Announcement, File, Task, StudentAnswer, Mark, Block, UrlLink
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from jinja2 import Environment
from django.contrib import auth


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
    if student_progress == 0:
        s_p = 0
    else:
        s_p = student_progress * 100 // count_lessons
    return render(request, "module/module_list.html", {"form": form, "modules": modules,
                                                       # "form_announcement": form_announcement,
                                                       # "announcements": announcements,
                                                       # "lesson": lesson,
                                                        "count_lessons":count_lessons,
                                                       "student_progress":student_progress,
                                                       "course": course,
                                                       "s_p": s_p,
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
    return HttpResponseRedirect(reverse('module:list', args=(id,)))


class CreateLesson(View):
    model = Lesson

    def get(self, request, m_id, id):
        module = Module.objects.get(id=m_id)
        course = Course.objects.get(id=id)
        return render(request, "module/lesson/create_lesson.html", {'form_lesson': LessonCreateForm(),
                                        'module': module,
                                        'course': course,
                                                                   })

    def post(self, request, m_id, id):
        module = Module.objects.get(id=m_id)
        course = Course.objects.get(id=id)
        form = LessonCreateForm(request.POST or None)
        if form.is_valid():
            lesson = Lesson()
            lesson.title = form.cleaned_data['title']
            lesson.description = form.cleaned_data["description"]
            lesson.short_description = form.cleaned_data['short_description']
            lesson.is_published = form.cleaned_data["is_published"]
            lesson.module_id = m_id
            lesson.save()
        return HttpResponseRedirect(reverse('module:list', args=(course.id,)))


# def create_block(request, l_id, id):
#     lesson = Lesson.objects.get(id=l_id)
#     course = Course.objects.get(id=id)
#     blocks = Block.objects.all().filter(lesson_id=l_id)
#     if request.method == "POST":
#         form = BlockCreateForm(request.POST or None)
#         if form.is_valid():
#             block = Block()
#             block.title = form.cleaned_data['title']
#             block.lesson_id = l_id
#             block.save()
#     return render(request, "module/lesson/block/block_create.html",
#                   {"lesson": lesson,
#                    "course": course,
#                    'blocks': blocks,
#                    "form": BlockCreateForm})


def create_task(request, id, m_id):
    module = Module.objects.get(id=m_id)
    course = Course.objects.get(id=module.course_id)
    if request.method == "POST":
        form = TaskForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            task = Task()
            task.title = form.cleaned_data['title']
            task.description = form.cleaned_data["description"]
            task.file = form.cleaned_data['file']
            task.time_deadline = form.cleaned_data['time_deadline']
            task.module_id = m_id
            task.save()
        return HttpResponseRedirect(reverse('module:list', args=(course.id,)))
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


def list_blocks(request, l_id, id):
    lesson = Lesson.objects.get(id=l_id)
    course = Course.objects.get(id=id)
    blocks = Block.objects.all().filter(lesson_id=l_id)
    return render(request, "module/lesson/block/list.html",
                  {"lesson": lesson,
                   "course": course,
                   'blocks': blocks,})



@login_required
def text_block_settings(request, l_id, id):
    user = request.user
    # Create the formset, specifying the form and formset we want to use.
    FileFormSet = formset_factory(FileForm, formset=BaseFileFormSet, extra=3)
    LinkFormSet = formset_factory(UrlLinkForm, formset=BaseLinkFormSet, extra=3)
    # Get our existing link data for this user.  This is used as initial data.
    lesson_ = Lesson.objects.get(id=l_id)
    # block = Block.objects.create(lesson_id=l_id)
    # files = File.objects.filter(block_id=block.id).order_by('id')
    # urls = UrlLink.objects.filter(block_id=block.id).order_by('id')
    # files_data = [{'title': f.title, 'file': f.file, } for f in files]
    # urls_data = [{'title_u': u.title, 'url': u.url, } for u in files]
    block = Block(lesson_id=l_id)
    files_data = []
    urls_data = []
    if request.method == 'POST':
        block_form = BlockForm(request.POST)
        file_formset = FileFormSet(request.POST or None, request.FILES or None)
        url_formset = LinkFormSet(request.POST or None)

        if block_form.is_valid() and file_formset.is_valid() and url_formset.is_valid():
            # Save user info
            block.title = block_form.cleaned_data.get('title')
            block.text_content = block_form.cleaned_data.get('text_content')
            block.save()
            # Now save the data for each form in the formset
            new_files = []
            for file_form in file_formset:
                title = file_form.cleaned_data.get('title')
                file = file_form.cleaned_data.get('file')
                if title and file:
                    new_files.append(File(block_id=block.id, title=title, file=file))
            new_links = []
            for url_form in url_formset:
                title = url_form.cleaned_data.get('title_u')
                url = url_form.cleaned_data.get('url')
                if title and url:
                    new_links.append(UrlLink(block_id=block.id, title=title, url=url))
            try:
                with transaction.atomic():
                    # Replace the old with the new
                    # Text.objects.filter(block_id=block.id).delete()
                    File.objects.bulk_create(new_files)
                    UrlLink.objects.bulk_create(new_links)
                    # And notify our users that it worked
                    messages.success(request, 'You have updated your profile.')
                    # return redirect(reverse('module:list_blocks', args=(id, lesson_.id,)))
            except IntegrityError:  # If the transaction failed
                messages.error(request, 'There was an error saving your profile.')
    else:
        block_form = BlockForm()
        file_formset = FileFormSet(initial=files_data)
        url_formset = LinkFormSet(initial=urls_data)
    return render(request, "module/lesson/block/block_create.html", {
        'block_form': block_form,
        'file_formset': file_formset,
        'url_formset': url_formset,
    })


#class CreateBlockAll(FormView):
    # form_class = BlockForm
    # template_name = "module/lesson/block/block_create.html"
    #
    # def get_context_data(self, **kwargs):
    #     context = super(CreateBlockAll, self).get_context_data(**kwargs)
    #     context['product_meta_formset'] = BlockInlineFormset()
    #     return context
    #
    # def post(self, l_id, id):
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     product_meta_formset = BlockInlineFormset(self.request.POST)
    #     if form.is_valid() and product_meta_formset.is_valid():
    #         return self.form_valid(form, product_meta_formset, l_id, id)
    #     else:
    #         return self.form_invalid(form, product_meta_formset, l_id, id)
    #
    # def form_valid(self, form, product_meta_formset,  l_id, id):
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     # saving ProductMeta Instances
    #     product_metas = product_meta_formset.save(commit=False)
    #     for meta in product_metas:
    #
    #         meta.save()
    #     return redirect(reverse("module:list_blocks", args=(Course.objects.get(id=id),)))
    #
    # def form_invalid(self, form, product_meta_formset,  l_id, id):
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               product_meta_formset=product_meta_formset,
    #                               course=Course.objects.get(id=id)
    #                               )
    #     )


#
# class TextAddView(TemplateView):
#     template_name = "module/lesson/block/add_text.html"
#
#     def get(self, request, id, block_id):
#         formset = TextFormSet(queryset=Text.objects.none())
#         return self.render_to_response({'bird_formset': formset, 'course': Course.objects.get(id=id)})
#
#     # Define method to handle POST request
#     def post(self, request, id, block_id):
#         formset = TextFormSet(data=self.request.POST)
#         # Check if submitted forms are valid
#         if formset.is_valid():
#             #formset.block = Block.objects.get(id=block_id)
#             formset.save()
#             return redirect(reverse_lazy("module:block_create"))
#
#         return self.render_to_response({'bird_formset': formset, 'course': Course.objects.get(id=id)})
#



def list_ans_from_task(request, id):
    answers = StudentAnswer.objects.all().filter(task_id=id)
    task = Task.objects.get(id=id)
    module = Module.objects.get(id= task.module_id)
    verified_answers = StudentAnswer.objects.all().filter(task_id=id, mark__isnull=False).order_by('-mark__time_create')
    unverified_answers = StudentAnswer.objects.all().filter(task_id=id, mark__isnull=True).order_by('-time_update')
    return render(request, "module/task/list_answer_from_task.html", {
        "answers": answers,
        "verified_answers": verified_answers,
        "unverified_answers": unverified_answers,
        "course": Course.objects.get(id=module.course_id) })


def edit_lesson(request, l_id, id):
    return render(request, "module/lesson/edit.html", {"lesson": Lesson.objects.get(id=l_id),
                                                       'course': Course.objects.get(id=id),
                                                              })


def edit_lesson_settings(request, l_id, id, ):
    try:
        lesson = Lesson.objects.get(id=l_id)
        module = Module.objects.get(id=lesson.module_id)
        course = Course.objects.get(id=id)
        form = LessonEditForm(request.POST or None, request.FILES or None, initial=
                                    {'title': lesson.title,
                                     'description': lesson.description,
                                     'short_description': lesson.short_description,
                                     'is_published': lesson.is_published,
                                     })

        blocks = Block.objects.all().filter(lesson_id=lesson.id)
        if form.is_valid():
            lesson.title = form['title'].value()
            lesson.description = form["description"].value()
            lesson.short_description = form['short_description'].value()
            lesson.is_published = form['is_published'].value()
            lesson.save()
            return render(request, "module/lesson/edit_lesson.html", {"lesson": lesson,
                                                               "module": module,
                                                               "item_id": module.course_id,
                                                               "form": form,
                                                               "course": course,
                                                               "blocks": blocks})
        else:
            return render(request, "module/lesson/edit_lesson.html", {"lesson": lesson,
                                                               "module": module,
                                                               "item_id": module.course_id,
                                                               "course": course,
                                                               "form": form, "blocks": blocks})
    except Lesson.DoesNotExist:
        return HttpResponseNotFound("<h2>Lesson not found</h2>")


def view_lesson(request, id, l_id):
    try:
        lesson = Lesson.objects.get(id=l_id)
        module = Module.objects.get(id=lesson.module_id)
        modules = Module.objects.all().filter(course_id=id)
        course = Course.objects.get(id=id)
        files = File.objects.all().filter(lesson_id=lesson.id)
        progress_is = get_progress(course.id, lesson.id, request.user.id)
        return render(request, "module/lesson/view_lesson.html", {"lesson": lesson,
                                                           "module": module,
                                                           "modules": modules,
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
            return render(request, "module/lesson/edit_lesson.html", {"lesson": lesson, "item_id": id})
        else:
            return render(request, "module/lesson/edit_lesson.html", {"lesson": lesson, "item_id": id})
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>Lesson not found</h2>")


def delete_module(request, id):
    try:
        module = Module.objects.get(id=id)
        id_course = module.course_id
        module.delete()
        return HttpResponseRedirect(reverse('module:list', args=(id_course,)))
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
    return HttpResponseRedirect(reverse('module:view_lesson', args=(course.id, lesson.id, )))


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
        return HttpResponseRedirect(reverse('module:list', args=(id_course,)))
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>task not found</h2>")


def content_course(request, id):
    course = Course.objects.get(id=id)
    modules = Module.objects.all().filter(course_id=id)
    return render(request, "module/content/base_nav.html", {'course': course,
                                                          "modules": modules,
                                                          })


def popup_form(request, id):
    # course = Course.objects.get(id=id)
    module = Module.objects.get(id=id)
    course = Course.objects.get(module=module)
    return render(request, "module/content/popup_form.html",
                  {'course': course,
                   'modules': course.module_set.all,
                   "module": module,
                   })


def student_progress_list(request, id):
    course = Course.objects.get(id=id)
    user = auth.get_user(request)
    marks = Mark.objects.all().filter(student_id=user.id, course_id=course.id)
    tasks = Task.objects.all().filter(module__course_id=id)
    mar = [i.mark for i in marks]
    if marks.count() != tasks.count():
        mar.append(0)
    z = zip(tasks, mar)
    r = [i for i in mar if i >= 1]
    res = sum(r)/len(r)

    student_answers = StudentAnswer.objects.all().filter(student_id=user.id, task__module__course_id=course.id)

    progress = РassingРrogress.objects.all().filter(course_id=id, student_id=user.id)

    return render(request, "module/student_progress/student_progress_list.html",
                  {'course': course,
                   'list_items': z,
                   'student_answers': student_answers,
                   'tasks': tasks,
                   'progress': progress,
                   'marks': marks,
                   'res': res})