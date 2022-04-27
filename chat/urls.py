from django.urls import path, include
from . import views

from django.conf.urls.static import static
from online_courses import settings


urlpatterns = [
    path(r'dialogs/', views.DialogsView.as_view(), name='dialogs'),
    path(r'dialogs/create/<user_id>/', views.CreateDialogView.as_view(), name='create_dialog'),
    path(r'dialogs/<chat_id>/', views.MessagesView.as_view(), name='messages'),
]