from django.shortcuts import render, redirect
from .forms import LoginForm, UserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

def login_view(request):
    if request.user.is_authenticated: 
        return redirect('index') 
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.warning(request, "로그인 정보가 올바르지 않습니다.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})