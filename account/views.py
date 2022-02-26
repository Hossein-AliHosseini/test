from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


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


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
