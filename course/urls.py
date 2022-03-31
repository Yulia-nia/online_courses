from django.urls import path
from . import views

from django.conf.urls.static import static
from online_courses import settings
from .views import pageNotFound

urlpatterns = [
    path('', views.index, name='index'),
    path('create_course/', views.create_course),
]

# debug with media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound