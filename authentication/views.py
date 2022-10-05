from curses.ascii import HT
import http
import logging

from django.shortcuts import HttpResponse, render

from .forms import LoginForm, RegisterForm, ForgotPasswordForm
from .services import registerUser, sendUserVerificationEmail, activateUser, sendResetPasswordLink
from .models import Accounts

# Create your models here.

def register_user(request):
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = registerUser(form.cleaned_data)
            if sendUserVerificationEmail(request, user):
                return HttpResponse('ok')
            else:
                HttpResponse("Nous n'avons pas pu vous envoyer un email de verification dans votre email. SVP contactez l'administrateur du site")
    else:
        form = RegisterForm()
    context['form'] = form
    return render(request, 'authentication/register_user.html', context)


def login_user(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return HttpResponse('ok')
    else:
        form = LoginForm()
    context['form'] = form    
    return render(request, 'authentication/login_user.html', context)

    
def activate_user(request, uidb64, token):
    if activateUser(uidb64, token):
        """ messages.success(request, 'congratulations! Your account is actived.')
        return redirect('login') """
        return HttpResponse('activate OK')
    else:
        """ messages.error(request, 'invalid activation link')
        return redirect('register') """
        return HttpResponse("Lien d'activation invalide")


def forgot_password(request):
    context = {}
    if request.method == 'POST':
        form = ForgotPasswordForm(request)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            sendResetPasswordLink(request, email)
            pass
    else:
        form = ForgotPasswordForm()
    context['form'] = form
    return render(request, 'authentication/forgot_password_user.html', context)


def reset_password_validate(request, uidb64, token):
    pass