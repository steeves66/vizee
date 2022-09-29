from django.shortcuts import render, HttpResponse
from .forms import RegisterForm
import logging

# Create your models here.

def register_user(request):
    context = {}
    if request.method == 'POST':
        numbers = request.POST.getlist('phone_numbers')
        numbers = ",".join(numbers)
        
        form = RegisterForm(request.POST, phone_numbers=numbers)
        
        return HttpResponse(form['phone_numbers'].value()) 
        
        """ form = RegisterForm(request.POST)
        if form.is_valid():
            return HttpResponse('ok') """
            
    else:
        form = RegisterForm()
    context['form'] = form
    return render(request, 'authentication/register.html', context)
