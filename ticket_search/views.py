import time

from django.contrib import messages
from django.shortcuts import render
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

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
