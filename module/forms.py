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


class LessonEditForm(forms.Form):
    title = forms.CharField(required=False, max_length=200, min_length=4, label='')
    description = forms.CharField(required=False, label='',
                                   widget=SummernoteWidget(attrs={'rows': 4,
                                                                  'summernote': {'width': '100%'}}))
    short_description = forms.CharField(required=False, label='',
                                   widget=forms.Textarea(attrs={'rows': 3}))
    is_published = forms.BooleanField(required=False, label='Опубликован')


class LessonForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=4,
                            label="Название", help_text="Введите название")
