# userauths/views.py
import email
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate , logout
from django.contrib import messages
from .forms import User, UserRegisterForm, UserLoginForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")
            
            # Authenticate using username
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('core:index')
    else:
        form = UserRegisterForm()

    return render(request, 'userauths/sign-up.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')

    if request.method == 'POST':
        email_or_username = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate: first try username, then email (optional)
        user = authenticate(username=email_or_username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('core:index')
        else:
            messages.error(request, "Invalid username/email or password.")
    
    return render(request, 'userauths/sign-in.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('userauths:sign-in')

@login_required
def account_view(request):
    return render(request, 'userauths/account.html')

@login_required
def orders_view(request):
    return render(request, 'userauths/orders.html')

@login_required
def vouchers_view(request):
    return render(request, 'userauths/vouchers.html')

@login_required
def wishlist_view(request):
    return render(request, 'userauths/wishlist.html')

@login_required
def settings_view(request):
    return render(request, 'userauths/settings.html')