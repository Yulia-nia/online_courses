from django.urls import path
from . import views

from django.conf.urls.static import static
from online_courses import settings
from .views import pageNotFound

urlpatterns = [
    path('', views.index, name='index'),
    path('create_course/', views.create_course),
    path('edit_course/<int:id>/', views.edit_course, name='edit'),
    path('main_settings/<int:id>/', views.settings_edit, name='setting'),
    path('delete/<int:id>/', views.delete_course),
]

# debug with media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound