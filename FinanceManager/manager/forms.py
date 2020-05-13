from django import forms
from . import models


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = models.Investment
        fields = ['company', 'units', 'start_date', 'end_date', 'remark']
        widgets = {
            'company': forms.Select(attrs={'class': ' sel form-control'}),
            'units': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control sel'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'sel form-control'}),
            'remark': forms.Textarea(attrs={'placeholder': 'Your Valuable Suggestion', 'class': 'form-control'}),

        }
