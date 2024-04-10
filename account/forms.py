from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):    
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email','password1', 'password2')
        
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control'}),
        }
        
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
