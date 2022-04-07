from django import forms


class ModuleForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=4,
                            label="Название", help_text="Введите название")


class LessonForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=4,
                            label="Название", help_text="Введите название")