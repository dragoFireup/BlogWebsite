from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):

    username = forms.CharField(forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username'}))
    email = forms.EmailField(forms.EmailInput(attrs={'class': 'input', 'placeholder': 'jane@doe.com'}),
                             max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password'}))
    password2 = forms.CharField(forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password Again'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)