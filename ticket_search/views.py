import time

from django.contrib import messages
from django.shortcuts import render

from .functions import get_condor


def home(request):

    page_title = get_condor()

    context = {
        'title': 'Home',
        'page_title': page_title
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
