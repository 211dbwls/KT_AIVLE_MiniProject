from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from . import views

# Create your views here.
def signup(request):
    if request.method == "POST":
        user_check = User.objects.filter(username=request.POST['UserID'])
        if len(user_check) == 0: 
            if request.POST['PW'] == request.POST['PWCheck']:
                user = User.objects.create_user(username=request.POST['UserID'], 
                                                password=request.POST['PW'], 
                                                email=request.POST['email'] )
                auth.login(request, user)
                return redirect('/')
            return render(request, 'accounts/signup.html', {'err':1})
        return render(request, 'accounts/signup.html', {'err':0})
    return render(request, 'accounts/signup.html')