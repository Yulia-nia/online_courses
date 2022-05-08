from django.urls import path, include
from . import views

from django.conf.urls.static import static
from online_courses import settings
from .views import pageNotFound, CourseAPIView

urlpatterns = [
    #path('', views.index, name='index'),
    path('course_catalog/', views.CatalogCourses.as_view(), name='catalog'),
    path('instructor_courses/', views.СoursesРarticularTeacher.as_view(), name='index'),
    path(r'instructor_courses/edit_course/<int:id>/', views.edit_course, name='edit'),
    path('delete/<int:id>/', views.delete_course, name='delete'),
    path('view_course/<int:id>/', views.view_course, name='view_course'),
    path('<int:c_id>/chat/dialog/', views.dialog, name='dialog'),

    path('<int:id>/chat/', include('chat.urls'), name='chat'),
    path('pass_course/<int:id>/', views.pass_course, name='pass_course'),
    path('<int:id>/info', views.info_course, name='info'),

    path('<int:id>/notifications', views.notifications_list_course, name='notifications_list'),
    path('<int:id>/students_list/create_notification/<int:s_id>/', views.create_notification, name='create_notification'),

    # path('dialogs/<int:d>/', views.dialog, name='dialog'),
    path('<int:id>/students_list/', views.students_list, name="students_list"),
    path('create_notification/<int:id>/', views.create_notification, name='create_notification'),

    # p


    # path('create_course/', views.create_course),
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