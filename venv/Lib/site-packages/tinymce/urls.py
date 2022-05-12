from django.urls import path
from .views import spell_check, filebrowser, css, spell_check_callback

urlpatterns = [
    path(r'spellchecker/', spell_check, name='tinymce-spellchecker'),
    path(r'filebrowser/', filebrowser, name='tinymce-filebrowser'),
    path(r'tinymce4.css', css, name='tinymce-css'),
    path(r'spellcheck-callback.js', spell_check_callback, name='tinymce-spellcheck-callback')
]
