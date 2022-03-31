from django import forms


class CourseForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)

