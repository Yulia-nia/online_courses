from django import forms


class CourseForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=4,
                            label="Название", help_text="Введите название")
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
                                  required=False,
                                  label="Краткое описание")

