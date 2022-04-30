from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_module, name='list'),
    path('create_module/', views.create_module, name='create'),
    # path('create_announcement/', views.create_announcement, name='create_announcement'),
    path('edit_module/<int:id>/', views.edit_module, name='edit_module'),
    path('delete_module/<int:id>/', views.delete_module),

    path('<int:id>/lesson_create/', views.create_lesson, name='create_lesson'),
    path('edit_lesson/<int:id>/', views.edit_lesson, name='edit_lesson'),

    path('view_lesson/<int:id>/', views.view_lesson, name='view_lesson'),

    path('progress/', views.progress, name='progress'),

    path('edit_module/<int:module_id>/edit_lesson/<int:id>/', views.edit_lesson_from_module, name='edit_lesson_from_module'),

    #path('delete/<int:id>/', views.delete_module),
]

