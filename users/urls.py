from django.urls import path, include
from django.views.generic import TemplateView
from users import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("accounts/", include("django.contrib.auth.urls")),
    path(r"register/", views.register, name="register"),
    path(r"register_student/", views.register_student, name="register_student"),
    path(r"register_instructor/", views.register_instructor, name="register_instructor"),
    path(r"edit_data", views.edit_data, name="edit_data"),
    path(r"profile/", views.profile, name="profile"),
]