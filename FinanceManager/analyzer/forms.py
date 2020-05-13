from django import forms
from . import models


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = models.Suggestion
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Topic', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'XXXX@XXX.COM', 'class': 'form-control'}),
            'user': forms.TextInput(attrs={'placeholder': 'Your Good Name', 'class': 'form-control'}),
            'suggestion': forms.Textarea(attrs={'placeholder': 'Your Valuable Suggestion', 'class': 'form-control'}),
        }

