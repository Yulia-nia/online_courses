from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.forms.formsets import BaseFormSet
from module.models import Block, File
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from tinymce.widgets import TinyMCE


class AnnouncementForm(forms.Form):
    content = forms.CharField(required=False, label='',
                                  widget=SummernoteWidget(attrs={'rows': 3,
                                                                 'summernote': {'width': '100%'}}))



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


class BlockForm(forms.Form):
    title = forms.CharField(required=False, max_length=200, min_length=4)
    text_content = forms.CharField(required=False, label='',
                              widget=SummernoteWidget(attrs={'rows': 4,
                                   'summernote': {'width': '50%'}})
                                )


class FileForm(forms.Form):
    title = forms.CharField(required=False, max_length=250, min_length=4)
    file = forms.FileField(required=False, label='')


class UrlLinkForm(forms.Form):
    title_u = forms.CharField(required=False, max_length=250, min_length=4)
    url = forms.URLField(widget=forms.URLInput(),required=False)


class BaseLinkFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        titles = []
        urls = []

        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                title = form.cleaned_data['title_u']
                url = form.cleaned_data['url']

                # Check that no two links have the same anchor or URL
                if title and url:
                    if title in titles:
                        duplicates = True
                    titles.append(title)

                    if url in urls:
                        duplicates = True
                    urls.append(url)

                if duplicates:
                    raise forms.ValidationError(
                        'Links must have unique anchors and URLs.',
                        code='duplicate_links'
                    )

                # Check that all links have both an anchor and URL
                if url and not title:
                    raise forms.ValidationError(
                        'All links must have an title.',
                        code='missing_title'
                    )
                elif title and not url:
                    raise forms.ValidationError(
                        'All links must have a url.',
                        code='missing_url'
                    )




class BaseFileFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        titles = []
        files = []

        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                title = form.cleaned_data['title']
                file = form.cleaned_data['file']

                # Check that no two links have the same anchor or URL
                if title and file:
                    if title in titles:
                        duplicates = True
                    titles.append(title)

                    if file in files:
                        duplicates = True
                    files.append(file)

                if duplicates:
                    raise forms.ValidationError(
                        'Links must have unique titles and files.',
                        code='duplicate_links'
                    )

                # Check that all links have both an anchor and URL
                if file and not title:
                    raise forms.ValidationError(
                        'All links must have an title.',
                        code='missing_title'
                    )
                elif title and not file:
                    raise forms.ValidationError(
                        'All links must have a file.',
                        code='missing_file'
                    )

