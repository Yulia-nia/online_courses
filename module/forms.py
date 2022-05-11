from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from django_summernote.widgets import SummernoteWidget

from module.models import Block, Text


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
    short_description = forms.CharField(required=False, label='', max_length=250,
                                   widget=forms.Textarea(attrs={'rows': 3}))
    is_published = forms.BooleanField(required=False, label='Опубликован')


class LessonCreateForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=4, label='')
    description = forms.CharField(required=False, label='',
                                  widget=SummernoteWidget(attrs={'rows': 4,
                                                                 'summernote': {'width': '100%'}}))
    short_description = forms.CharField(required=False, label='', max_length=250,
                                        widget=forms.Textarea(attrs={'rows': 3}))
    is_published = forms.BooleanField(required=False, label='Опубликован')


class BlockCreateForm(forms.Form):
    # class Meta:
    #     model = Block
    #     fields = ('title',)
    title = forms.CharField(required=False, max_length=200, min_length=4)


class BlockEditForm(forms.Form):
    title = forms.CharField(required=False, max_length=200, min_length=4, label='')


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


# class TextLessonForm(forms.Form):
#     content = forms.CharField(required=False, label='',  widget=SummernoteWidget(attrs={'rows': 4,
#                                     'summernote': {'width': '100%'}}
#                                    ))

# class TextLessonForm(forms.ModelForm):
#     class Meta:
#       model = Text
#       fields = [content]


class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ('title',)


class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ('content',)


BlockInlineFormset = inlineformset_factory(Block,
                                           Text,
                                           form=TextForm,
                                           extra=5,)

