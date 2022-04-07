from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
# Create your views here.
from course.models import Course
from module.forms import ModuleForm
from module.models import Module, Lesson


def list_module(request, id):
    #course = Course.objects.get(id=id)
    form = ModuleForm()
    modules = Module.objects.all()
    # in case to filter by id
    modules = Module.objects.filter(course_id=id)
    return render(request, "module/module_list.html", {"form": form, "modules": modules, "item_id": id})


def create_module(request, id):
    if request.method == "POST":
        module = Module()
        module.title = request.POST.get("title")
        module.course_id = id
        module.save()
    return HttpResponseRedirect(reverse('list', args=(id,)))
