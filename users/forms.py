from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user',]
        labels = {
            'real_name': 'Name',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'image': forms.FileInput(),
        }