from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class CourseForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=4,
                            label="Название", help_text="Введите название")
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
                                  required=False,
                                  label="Краткое описание")


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
                                   widget=SummernoteWidget(attrs={'rows': 5})
                                  )

    how_training = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'rows': 3}))
    what_you_get = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'rows': 3}))
    LEVEL_CHOICES = (
        ('1', u"для начаниющих"),
        ('2', u"для продолжающих"),
        ('3', u"для продвинутых"),
    )
    level = forms.ChoiceField(label='', choices=LEVEL_CHOICES)



