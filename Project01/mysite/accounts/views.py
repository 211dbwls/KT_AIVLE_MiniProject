from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    return render(request, 'index.html')

# 로그인
def login_view(request):
    if request.user.is_authenticated: 
        return redirect('index') 
    
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        signup_form = SignUpForm()
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
        signup_form = SignUpForm()

    return render(request, 'login.html', {'login_form': login_form, 'signup_form':signup_form})

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('index')

# 회원가입
def signup(request):
    return render(request, 'login.html')
    