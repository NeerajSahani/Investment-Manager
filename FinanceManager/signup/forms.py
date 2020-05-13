from django.contrib.auth.forms import UserCreationForm
from . import models
from django import forms


class SignupForm(UserCreationForm):
    class Meta:
        model = models.CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_image', 'gender', 'occupation',
                  'date_of_birth', 'mobile', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'type': 'text', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
            'profile_image': forms.FileInput(),
            'gender': forms.Select(attrs={'placeholder': 'select'}),
            'occupation': forms.TextInput(attrs={'placeholder': 'Occupation'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Mobile Number'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'vDateField'})
        }
