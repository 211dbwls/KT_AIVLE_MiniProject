from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

# 로그인
def login_view(request):
    if request.user.is_authenticated: 
        return redirect('index') 
    
    signup_form = SignUpForm()
    
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.warning(request, "로그인 정보가 올바르지 않습니다.")
    else:
        login_form = LoginForm()

    return render(request, 'login.html', {'login_form': login_form, 'signup_form':signup_form})

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('index')

# 회원가입
def signup(request):
    login_form = LoginForm()
    
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            return redirect('index')
        else:
            print(signup_form.errors)
            messages.warning(request, '회원가입에 실패했습니다.')
    else:
        signup_form = SignUpForm()
    
    return render(request, 'login.html', {'login_form': login_form, 'signup_form':signup_form})
    