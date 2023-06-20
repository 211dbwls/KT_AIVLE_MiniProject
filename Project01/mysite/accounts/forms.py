from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# 로그인폼
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

# 회원가입폼
class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Username')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Check Password', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email Address')
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
