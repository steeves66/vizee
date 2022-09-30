import http
from django.shortcuts import render, HttpResponse
from .forms import RegisterForm, LoginForm
from .services import registerUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages, auth
import logging

# Create your models here.

def register_user(request):
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            registerUser(form.cleaned_data)
            return HttpResponse('ok')
    else:
        form = RegisterForm()
    context['form'] = form
    return render(request, 'authentication/register_user.html', context)

def login_user(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid:
            return HttpResponse('ok')
    else:
        form = LoginForm()
    context['form'] = form
    return render(request, 'authentication/login_user.html', context)
        

def login(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
    else:
        form = LoginForm()
    context['form'] = form    
    return render(request, 'authentication/login_user.html', context)
