from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Accounts(AbstractBaseUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    phone_numbers = models.CharField(max_length=255)
    agree = models.BooleanField(blank=True)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'