from django.shortcuts import render
from django.contrib import messages


def home(request):

    context = {
        'title': 'Home'
    }
    messages.error(request, 'Hello')
    return render(request, 'ticket_search/home.html', context)


def about(request):

    context = {
        'title': 'About'
    }

    messages.info(request, 'Hello')
    messages.warning(request, 'Hello world')
    return render(request, 'ticket_search/about.html', context)
