from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import (UserCreationForm,
                                       AuthenticationForm,
                                       PasswordChangeForm)
from django.views.generic.edit import CreateView
from django.contrib.auth import login, logout, update_session_auth_hash
from django.http import HttpResponseRedirect
from django.contrib import messages


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


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
