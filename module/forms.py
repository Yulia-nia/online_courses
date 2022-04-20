from django import forms
from django_summernote.widgets import SummernoteWidget


class AnnouncementForm(forms.Form):
    content = forms.CharField(label='', widget=SummernoteWidget(attrs={
                                                                       'summernote': {
                                                                           'width': '100%',
                                                                           'height': '280px'
                                                                           }}))


class ModuleForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=4,
                            label="Название", help_text="Введите название")


class LessonForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=4,
                            label="Название", help_text="Введите название")
