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


class TaskForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=4, label='')
    description = forms.CharField(max_length=200, label='',
                                  widget=forms.Textarea(attrs={'rows': 3}),
                                  required=False)
    file = forms.FileField(required=False, label='')
    time_deadline = forms.DateTimeField( input_formats=['%Y-%m-%d %H:%M'],required=False)


class AnswerTaskForm(forms.Form):
    description = forms.CharField(max_length=200, label='',
                                  widget=forms.Textarea(attrs={'rows': 3}),
                                  required=False)
    file = forms.FileField(required=False, label='')


class MarkForm(forms.Form):
    mark = forms.IntegerField(label='', required=False)


class TextLessonForm(forms.Form):
    content = forms.CharField(required=False, label='',  widget=SummernoteWidget(attrs={'rows': 4,
                                    'summernote': {'width': '100%'}}
                                   ))
