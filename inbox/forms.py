from django import forms
from .models import InboxMessage

class InboxNewMessageForm(forms.ModelForm):
    class Meta:
        model = InboxMessage
        fields = ['body']
        labels = {
            'body': '',
        }
        widgets = {
            'body': forms.Textarea(attrs={'class':'font1','placeholder': 'Write a message... '}),
        }