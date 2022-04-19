from django import forms


class CourseForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=4,
                            label="Название", help_text="Введите название")
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
                                  required=False,
                                  label="Краткое описание")


class SettingsForm(forms.Form):
    learning_format = forms.CharField(required=False, max_length=200, min_length=4, label="Формат обучения")
    subject = forms.CharField(required=False, max_length=200, min_length=4, label="Предмет")
    language = forms.CharField(required=False, max_length=200, min_length=4, label="Язык")
    image = forms.ImageField(required=False)
    is_published = forms.BooleanField(required=False)


