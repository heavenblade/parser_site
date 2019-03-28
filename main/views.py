from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Grammar
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Views
def homepage(request):
    return(render(request = request, template_name = "main/home.html"))

def register(request):
    if (request.method == "POST"):
        form = UserCreationForm(data = request.POST)
        if (form.is_valid()):
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Welcome {username}")
            login(request, user)
            return(redirect("main:homepage"))
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")
    form = UserCreationForm
    return(render(request = request, template_name = "main/register.html", context = {"form": form}))

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return(redirect("main:homepage"))

def login_request(request):
    if (request.method == "POST"):
        form = AuthenticationForm(request, data = request.POST)
        if (form.is_valid()):
            usr = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            user = authenticate(username = usr, password = pwd)
            if (user is not None):
                login(request, user)
                messages.success(request, f"You are now logged in as {usr}")
                return(redirect("main:homepage"))
            else:
                messages.error(request, f"Invalid username or password")
    form = AuthenticationForm()
    return(render(request = request, template_name = "main/login.html", context = {"form": form}))
