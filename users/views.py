from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from course.models import Course
from users.forms import CustomUserCreationForm, UserEditForm
from django.contrib.auth.models import Group

from users.models import User, BookmarkCourse


def dashboard(request):
    return render(request, "users/dashboard.html")


def profile(request):
    user = User.objects.get(username=request.user.username)
    courses = []
    for i in BookmarkCourse.objects.all().filter(user=user):
        courses.append(Course.objects.get(id=i.obj_id))
    return render(request, "users/profile.html", {'user': user, "courses": courses})


def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name='Ученик'))
            login(request, user)
        return redirect(reverse("dashboard"))


def edit_data(request):
    # if request.method == "GET":
    #     return render(
    #         request, "users/edit_data.html",
    #         {"form": UserEditForm}
    #     )
    # else:
    user = User.objects.get(username=request.user.username)
    form = UserEditForm(request.POST or None, request.FILES or None,
                            initial=
                            {'email': user.email,
                             'bio': user.bio,
                             'avatar': user.image_pic
                             })
    if form.is_valid():
        user.email = form['email'].value()
        user.bio = form["bio"].value()
        user.image_pic = form['avatar'].value()
        user.save()
    return render(request, "users/edit_data.html", {'form': form})


