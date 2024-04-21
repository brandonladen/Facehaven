from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register_user')
        
        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken")
            return redirect('register_user')
        
        # Create the user object
        user = User.objects.create_user(username=username, 
                                        email=email,
                                        first_name=first_name,
                                        last_name=last_name,
                                        password=password)
        user.save()
        
        messages.success(request, "Successfully signed up. You can now login.")
        return redirect('login')
    
    return render(request, 'account/authentication.html')


from django.contrib import messages

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Manually authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user
            login(request, user)
            messages.success(request, "Successfully logged in")
            if not user.is_superuser:
                # return redirect('submit_child')
                return render(request, 'account/who.html')
            else:
                return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'account/authentication.html')

def authentication(request):
    return render(request, 'account/authentication.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('home')