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
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_check = forms.CharField(label='Check Password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email Address')
    phone_number = forms.CharField(label='Phone number', max_length=11)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password_check', 'first_name', 'last_name', 'email', 'phone_number']
