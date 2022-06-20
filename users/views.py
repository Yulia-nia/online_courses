from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from course.models import Course
from users.forms import CustomUserCreationForm, UserEditForm, CustomInstructorCreationForm
from django.contrib.auth.models import Group

from users.models import User, BookmarkCourse


def dashboard(request):
    return render(request, "course/course_catalog.html")


def profile(request):
    user = User.objects.get(username=request.user.username)
    # курсы что проходишь
    courses = []
    for i in BookmarkCourse.objects.all().filter(user=user):
        courses.append(Course.objects.get(id=i.obj_id))

    courses_instructor = Course.objects.all().filter(author_id=user.id)

    c_s = Course.objects.all().filter(coursenrollment__students=user)
    # c_s = []
    # for i in courses_student:
    #     for s in i.coursenrollment.students.all():
    #         if s.id == user.id:
    #             c_s.append(i)

    return render(request, "users/profile.html", {'user': user, "courses": courses,
                                                  "c_s": c_s,
                                                  'courses_instructor': courses_instructor})


def register(request):
    return render(request, "users/register.html")

    # if request.method == "GET":
    #     return render(
    #         request, "users/register.html",
    #         {"form": CustomUserCreationForm}
    #     )
    # elif request.method == "POST":
    #     form = CustomUserCreationForm(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         user.groups.add(Group.objects.get(name='Ученик'))
    #         login(request, user)
    #     return redirect(reverse("dashboard"))


def register_instructor(request):
    if request.method == "GET":
        return render(
            request, "users/register_instructor.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomInstructorCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name='Преподаватель'))
            login(request, user)
        return redirect(reverse("index"))


def register_student(request):
    if request.method == "GET":
        return render(
            request, "users/register_student.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name='Ученик'))
            login(request, user)
        return redirect(reverse("index"))


def edit_data(request):
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
    return render(request, "users/edit_data.html", {'form': form, 'user': user})
