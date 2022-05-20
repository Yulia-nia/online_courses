from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'module'

urlpatterns = [

    # module
    path('create_module/', views.create_module, name='create'),

    path('delete_module/<int:id>/', views.delete_module),

    # task
    path('<int:m_id>/create_task/', views.create_task, name='create_task'),
    path('edit_task/<int:id>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:id>/', views.delete_task, name='delete_task'),

    path('view_task/<int:id>/', views.TaskView.as_view(), name='view_task'),

    path('ansewers_students/', views.list_answers_tasks, name='list_answers'),
    path('ansewers_students/<int:id>/task/', views.list_ans_from_task, name='list_ans_from_task'),
    path(r'estimate/<int:a_id>/', views.EstimateView.as_view(), name='estimate'),

    # lesson
    path('<int:m_id>/lesson_create/', views.CreateLesson.as_view(), name='create_lesson'),
    #path('<int:m_id>/lesson_create/', views.create_lesson, name='create_lesson'),

    path('edit_lesson_all/<int:l_id>/', views.edit_lesson, name='edit_lesson'),
    path('<int:l_id>/edit_lesson/', views.edit_lesson_settings, name='edit_lesson_settings'),

    path('<int:l_id>/list_blocks/', views.list_blocks, name='list_blocks'),


    path('<int:l_id>/block_create/', views.text_block_settings, name='block_create'),


    #path('<int:block_id>/add_text/', views.TextAddView.as_view(), name="add_text"),


    path('view_lesson/<int:l_id>/', views.view_lesson, name='view_lesson'),

    path('progress/', views.progress, name='progress'),

    path('edit_module/<int:module_id>/edit_lesson/<int:id>/', views.edit_lesson_from_module, name='edit_lesson_from_module'),


    path('content/', views.content_course, name='content_course'),
    path('popup/', views.popup_form, name='popup_form'),
    # progress student
    path('progress_list/<int:s_id>/', views.student_progress_list, name='student_progress_list'),
    path('edit_module/<int:m_id>/', views.edit_module, name='edit_module'),
    path('', views.list_module, name='list'),
    path('summernote/', include('django_summernote.urls')),
    #path('delete/<int:id>/', views.delete_module),


path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

