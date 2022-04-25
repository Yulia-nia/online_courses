from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import User

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'location')
       #etc etc, other fields you want displayed on the form)

#
# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         fields = UserCreationForm.Meta.fields + ("email",)


class CustomUserEditForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'location', 'bio', 'birth_date')


class UserEditForm(forms.Form):
    email = forms.CharField()
    bio = forms.CharField(required=False,  widget=SummernoteWidget(attrs={'rows': 4,
                                    'summernote': {'width': '100%'}}
                                   ))
    avatar = forms.ImageField(required=False)

