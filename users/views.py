from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username') 
            form.save()
            messages.success(request, f'User {user_name} is succesfully registered')
            return redirect('home')
    else:
        form = UserRegisterForm()
    context = { 
        'title' : 'Registration',
        'form' : form
    }
    return render(request, 'users/register.html', context)
