from django.urls import path, include
from django.views.generic import TemplateView
from users import views


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(r"register/", views.register, name="register"),
    path(r"edit_data", views.edit_data, name="edit_data"),
    path(r"profile/", views.profile, name="profile"),

]