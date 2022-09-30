from django.contrib import messages, auth
from django import forms
from .models import Accounts
import re


class RegisterForm(forms.ModelForm):
    # nom = forms.CharField()
    # prenom = forms.CharField()
    # email = forms.CharField(widget=forms.EmailInput)
    # username = forms.CharField(max_length=100)
    # password = forms.CharField(widget=forms.PasswordInput)
    # confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8, error_messages={'min_length': 'Votre mot de passe doit contenir au moins 8 caractères.'})
    # phone_numbers = forms.CharField()
    # agree = forms.BooleanField()

    confirm_password = forms.CharField()
    
    class Meta:        
        model = Accounts
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_numbers', 'password')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages = {'required': 'Veuillez saisir un email'}
        self.fields['first_name'].error_messages = {'required': 'Veuillez saisir un nom'}
        self.fields['last_name'].error_messages = {'required': 'Veuillez saisir un prénom'}
        self.fields['password'].error_messages = {'required': 'Veuillez saisir un mot de passe'}
        self.fields['confirm_password'].error_messages = {'required': 'Veuillez saisir un mot de passe de confirmation'}
        self.fields['phone_numbers'].error_messages = {'required': 'Veuillez saisir un numero pour vous contacter'}

    def clean_email(self):
        email = self.cleaned_data['email']
        """ if email is None:
            raise forms.ValidationError('Vous devez avoir un email, veuillez saisir un email') """
        user = Accounts.objects.filter(email= email).exists()
        if(user):
            raise forms.ValidationError('Cet email est utilisé, veuillez saisir un email non utilisé.')
        regex = '^[a-z0-9]+[\.-_]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.fullmatch(regex, email)):
            raise forms.ValidationError("Votre email n'a pas le bon format, veuillez saisir un email valide")
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user_name = Accounts.objects.filter(username=username).exists()
        if user_name:
            raise forms.ValidationError('Ce surnom est utilisé, veuillez saisir un surnom non utilisé.')
        if len(username) < 3:
            raise forms.ValidationError('Votre surnom doir contenir au moins 3 caractères.')
        return username
    
    def clean_phone_numbers(self):
        phone_numbers = self.cleaned_data['phone_numbers']
        if len(phone_numbers) < 10:
            raise forms.ValidationError('Votre numero doit être ne doit pas inferieur à 10 chiffres')
        if len(phone_numbers) > 15:
            raise forms.ValidationError('Votre numero doit être ne doit pas superieur à 15 chiffres')
        regex = '^[0-9]{10,15}$'
        if not (re.fullmatch(regex, phone_numbers)):
            raise forms.ValidationError('Le numero ne doit pas contenir des lettres')
        return phone_numbers
    
    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password and len(password) < 8:
            self.add_error('password', 'Votre mot de passe doit avoir au moins 8 caractères')
            
        if confirm_password and len(confirm_password) < 8:
            self.add_error('confirm_password', 'Votre mot de passe doit avoir au moins 8 caractères')
            
        if(password != confirm_password):
            raise forms.ValidationError('Votre mot de passe et sa confirmation ne correspondent pas')



class LoginForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ('email', 'password')
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages = {'required': ''}
        self.fields['password'].error_messages = {'required': ''}
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if email is None:
            raise forms.ValidationError("Veuillez saisir un email")
        return email
      
    def clean_password(self):
        password = self.cleaned_data['password']
        if password is None:
            raise forms.ValidationError("Veuillez saisir un mot de passe")
        return password
    
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
            
        user = Accounts.objects.filter(email=email).first()
        if not user:
            self.add_error('email', 'informations d\'identification invalides: email n\'existe pas')
        else: 
            if not user.check_password(password):
                self.add_error('password', 'informations d\'identification invalides: mot de passe incorrect')
        
        