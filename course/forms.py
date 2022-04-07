from django import forms


class CourseForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=4,
                            label="Название", help_text="Введите название")
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
                                  required=False,
                                  label="Краткое описание")


# class SettingsForm(forms.Form):
#     learning_format = forms.CharField(max_length=200, min_length=4, label="Формат обучения")
#     subject = forms.CharField(max_length=200, min_length=4, label="Предмет")
#     language = forms.CharField(max_length=200, min_length=4, label="Язык")

