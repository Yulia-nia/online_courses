from django.forms import ModelForm, Textarea
from chat.models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}
        widgets = {
            'message': Textarea(attrs={'cols': 80, 'rows': 1}),
        }

