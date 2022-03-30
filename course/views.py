from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404

# Create your views here.


def index(request):
    return render(request, "course/index.html")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')