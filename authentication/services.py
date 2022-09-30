from .models import Accounts

def registerUser(cleaned_data):
    user = Accounts()
    user.first_name = cleaned_data.get('first_name')
    user.last_name = cleaned_data.get('last_name')
    user.username = cleaned_data.get('username')
    user.phone_numbers = cleaned_data.get('phone_numbers')
    user.email = cleaned_data.get('email')
    user.save(commit=False)
    password = cleaned_data.get('password')
    user.set_password(password)
    return user

def authenticateUser(cleaned_data):
    user = Accounts()
    email = cleaned_data.get('email')
    password = cleaned_data.get('password')