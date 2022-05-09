from django.urls import path
from . import views


app_name = 'module'

urlpatterns = [

    # module
    path('create_module/', views.create_module, name='create'),
    path('edit_module/<int:id>/', views.edit_module, name='edit_module'),
    path('delete_module/<int:id>/', views.delete_module),

    # task
    path('create_task/', views.create_task, name='create_task'),
    path('edit_task/<int:id>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:id>/', views.delete_task, name='delete_task'),

    path('view_task/<int:id>/', views.TaskView.as_view(), name='view_task'),

    path('ansewers_students/', views.list_answers_tasks, name='list_answers'),
    path('ansewers_students/<int:id>/task/', views.list_ans_from_task, name='list_ans_from_task'),
    path(r'estimate/<int:id>/', views.EstimateView.as_view(), name='estimate'),

    # lesson
    path('<int:m_id>/lesson_create/', views.create_lesson, name='create_lesson'),
    path('edit_lesson/<int:id>/', views.edit_lesson, name='edit_lesson'),
    path('view_lesson/<int:id>/', views.view_lesson, name='view_lesson'),

    path('progress/', views.progress, name='progress'),

    path('edit_module/<int:module_id>/edit_lesson/<int:id>/', views.edit_lesson_from_module, name='edit_lesson_from_module'),


    path('content/', views.content_course, name='content_course'),
    path('', views.list_module, name='list'),
    #path('delete/<int:id>/', views.delete_module),
]

