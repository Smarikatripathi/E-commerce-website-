#Forms.py defines the structure, validation, and connection to the database model.
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(UserCreationForm): #UserRegisterForm inherits from UserCreationForm
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'})) #widget allows you to add HTML attributes
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    class Meta: #The Meta class links the form to your custom User model (get_user_model()) and specifies which fields are included.
        model = get_user_model()
        fields = ['username', 'email']

class UserLoginForm(AuthenticationForm): #UserLoginForm inherits from AuthenticationForm
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']       