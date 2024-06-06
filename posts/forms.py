from django import forms
from django.forms import ModelForm
from .models import *

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['url','content','tags']
        labels = {
            'content': 'Caption',
            'tags':'Category',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5,'cols': 25,'placeholder': 'Add a Caption... ','class':'form-control font1 text-3xl',}),
            'url': forms.TextInput(attrs={'placeholder': 'Add a URL... '}),
            'tags':forms.CheckboxSelectMultiple(attrs={'class':'form-control',}),
        }
        
        
class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content','tags']
        labels = {
            'content': '',
            'tags':'Category',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5,'cols': 25,'class':'form-control font1 text-3xl',}),
            'tags':forms.CheckboxSelectMultiple(attrs={'class':'form-control',}),
        }
        

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': '',
        }
        widgets = {
            'body': forms.TextInput(attrs={'class':'flex-1 display-flex font1','placeholder': 'Add a Comment... '}),
        }
        

class ReplyCreateForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        labels = {
            'body': '',
        }
        widgets = {
            'body': forms.TextInput(attrs={'class':'font1','placeholder': 'Add a Reply... '}),
        }