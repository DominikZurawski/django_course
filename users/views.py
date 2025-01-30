from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.contrib.auth import logout
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Welcome {username}, your account has been created! You are now able to log in.')
            return redirect('food:index')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return render(request, 'users/logout.html', {})

@login_required
def profilepage(request):
    return render(request, 'users/profile.html')