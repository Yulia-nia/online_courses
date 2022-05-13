from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from course.models import Comment


class CourseForm(forms.Form):
    title = forms.CharField(max_length=64, min_length=4, label='')
    description = forms.CharField(max_length=200, label='',
                                  widget=forms.Textarea(attrs={'rows': 3}),
                                  required=False)


class NotificationForm(forms.Form):
    content = forms.CharField(max_length=200, label='',
                                  widget=forms.Textarea(attrs={'rows': 2}),
                                  required=False)


class SettingsForm(forms.Form):
    learning_format = forms.CharField(required=False, max_length=200, min_length=4, label='')
    will_learn = forms.CharField(required=False, label='',
                                 widget=forms.Textarea(attrs={'rows': 3}))
    necessary_training = forms.CharField(required=False, label='',
                                         widget=forms.Textarea(attrs={'rows': 3}))

    subject = forms.CharField(required=False, max_length=200, min_length=4, label='')
    language = forms.CharField(required=False, max_length=200, min_length=4, label='')
    image = forms.ImageField(required=False, label='')
    is_published = forms.BooleanField(required=False, label='Опубликован')

    about_course = forms.CharField(required=False, label='',
                                   widget=SummernoteWidget(attrs={'rows': 4,
                                    'summernote': {'width': '100%'}}
                                   ))

    how_training = forms.CharField(required=False, label='',  widget=SummernoteWidget(attrs={'rows': 4,
                                    'summernote': {'width': '100%'}}
                                   ))
    what_you_get = forms.CharField(required=False, label='',  widget=SummernoteWidget(attrs={'rows': 4,
                                    'summernote': {'width': '100%'}}
                                   ))
    LEVEL_CHOICES = (
        ('1', u"для начаниющих"),
        ('2', u"для продолжающих"),
        ('3', u"для продвинутых"),
    )
    level = forms.ChoiceField(label='', choices=LEVEL_CHOICES, required=False)

    COURSE_CHOICES = (
        ('0', u"идет разработка курса"),
        ('1', u"идет набор на курс"),
        ('2', u"курс начался"),
        ('3', u"курс закончился"),
    )
    active_level = forms.ChoiceField(label='', choices=COURSE_CHOICES, required=False)



class CoursEnrollmentForm(forms.Form):
    time_end = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'], required=False, label='')


class CommentForm1(forms.Form):
    parent_comment = forms.IntegerField(
        widget=forms.HiddenInput,
        required=False
    )
    comment_area = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'rows': 3})
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)

