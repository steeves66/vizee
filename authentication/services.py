from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import Accounts


def registerUser(cleaned_data):
    user = Accounts()
    user.first_name = cleaned_data.get('first_name')
    user.last_name = cleaned_data.get('last_name')
    user.username = cleaned_data.get('username')
    user.phone_numbers = cleaned_data.get('phone_numbers')
    user.email = cleaned_data.get('email')
    password = cleaned_data.get('password')
    user.set_password(password)
    user.save()
    return user


def sendUserVerificationEmail(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token =  default_token_generator.make_token(user)
    print("----------------------- uid: "+ uid)
    print("----------------------- token: "+ token)
    current_site = get_current_site(request)
    email_context = {
        'user': user,
        'uid': uid,
        'token': token,
        'current_site': current_site
    }
    email_subject = "Vizee: Activation de votre compte"
    email_html_message = render_to_string('mails/user_verification_email.html', email_context)
    email_text_message = strip_tags(email_html_message)
    to_email = user.email
    email = EmailMultiAlternatives(email_subject, email_text_message, to=[to_email])
    email.attach_alternative(email_html_message, "text/html")
    email.content_subtype = "html"  # Main content is now 
    email.send()
    return True

""" def sendUserVerificationEmail_old(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token =  default_token_generator.make_token(user)
    print("----------------------- uid: "+ uid)
    print("----------------------- token: "+ token)
    current_site = get_current_site(request)
    email_context = {
        'user': user,
        'uid': uid,
        'token': token,
        'current_site': current_site
    }
    email_subject = "Vizee: Activation de votre compte"
    email_message = render_to_string('mails/user_verification_email.html', email_context)
    to_email = user.email
    email = EmailMessage(email_subject, email_message, to=[to_email])
    email.send()

    return True """

def activateUser(uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Accounts.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Accounts.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    else:
        return False
    

def sendResetPasswordLink(request, email):
    user = Accounts.objects.filter(email = email).first()
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token =  default_token_generator.make_token(user)
    current_site = get_current_site(request)
    email_context = {
        'user': user,
        'uid': uid,
        'token': token,
        'current_site': current_site
    }
    email_subject = "Vizee: Activation de votre compte"
    email_message = render_to_string('mails/reset_password_email.html', email_context)
    to_email = user.email
    email = EmailMessage(email_subject, email_message, to=[to_email])
    email.send()

    return True


