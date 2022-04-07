from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_module, name='list'),
    path('create_module/', views.create_module, name='create'),
    #path('edit_module/<int:id>/', views.edit_module, name='edit_mod'),
    #path('delete/<int:id>/', views.delete_module),
]

