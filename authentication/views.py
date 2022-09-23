from django.shortcuts import render, HttpResponse
from .forms import RegisterForm

# Create your models here.

def register_user(request):
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            return HttpResponse('ok')
    else:
        form = RegisterForm()
    context['form'] = form
    return render(request, 'authentication/register.html', context)
       