from django.urls import path, include
from . import views

from django.conf.urls.static import static
from online_courses import settings
from .views import pageNotFound, CourseAPIView

urlpatterns = [
    path('', views.index, name='index'),
    path('create_course/', views.create_course),

    path('edit_course/<int:id>/', views.edit_course, name='edit'),
    path('main_settings/<int:id>/', views.settings_edit, name='setting'),
    path('delete/<int:id>/', views.delete_course),
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