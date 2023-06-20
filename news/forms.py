from django import forms
from .models import CommunityNews

class CommunityNewsCreateForm(forms.ModelForm):
    class Meta:
        model = CommunityNews
        fields = ['banner', 'title', 'category', 'description', 'content']
