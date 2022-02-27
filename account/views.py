from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import (UserCreationForm,
                                       AuthenticationForm,
                                       PasswordChangeForm)
from django.views.generic.edit import CreateView
from django.contrib.auth import (login,
                                 logout,
                                 update_session_auth_hash,
                                 authenticate)
from django.http import HttpResponseRedirect
from django.contrib import messages

from .forms import CustomUserCreationForm


def home(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request,
                  'registration/login.html',
                  {'form': form})


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/home')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,
                             'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def handle_404(request):
    return render(request, '404.html')


# def handle_500(request):
#     return render(request, '500.html')


def handle_403(request):
    return render(request, '403.html')
