from django.urls import path, include
from . import views

from django.conf.urls.static import static
from online_courses import settings
from .views import pageNotFound, CourseAPIView


urlpatterns = [

    path('', views.index, name='index'),
    path('course_catalog/', views.catalog_courses, name='catalog'),
    path('view_course/<int:id>/', views.view_course, name='view_course'),
    path('pass_course/<int:id>/', views.pass_course, name='pass_course'),

    path('<int:id>/students_list/', views.students_list, name="students_list"),
    path('create_course/', views.create_course),
    path('edit_course/<int:id>/', views.edit_course, name='edit'),
    path('delete/<int:id>/', views.delete_course),

    path('main_settings/<int:id>/', views.settings_edit, name='setting'),

    path('<int:id>/module/', include('module.urls'), name='module'),

    path('<int:id>/check_list/', views.check_list, name='check_list'),

    path('<int:id>/announcement_list/', views.announcement_list, name='announcement_list'),
    path('<int:id>/announcement_list/create_announcement/', views.create_announcement, name='create_announcement'),

    path('api/v1/courselist/', CourseAPIView.as_view()),
    #path('module/<int:id>/', views.module_course, name='module'),
]

# debug with media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound