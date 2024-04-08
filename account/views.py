from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Signed up")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }        
    return render(request, 'account/signup.html', context)

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(password=password, username=username)
            login(request, user)
            messages.success(request, "Successfully Logged in")
            if not request.user.is_superuser:
                # return redirect('submit_child')
                return render(request, 'account/who.html')
            else:
                return redirect('admin_dashboard')
    else:
        form = UserLoginForm()
        
    context = {
        'form': form
    }
    return render(request, 'account/login.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('home')