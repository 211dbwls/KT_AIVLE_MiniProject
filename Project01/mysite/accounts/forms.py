from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_check = forms.CharField(label='Check Password', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email Address')
    phone_number = forms.CharField(label='Phone number', max_length=11)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password_check', 'email', 'phone_number']
