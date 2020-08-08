import time

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import SearchQueryForm
from .functions import get_condor


def home(request):

    # page_title = get_condor()

    context = {
        'title': 'Home',
        #'page_title': page_title
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


def search(request):

    if request.method == 'POST':
        return redirect('results')
        
    form = SearchQueryForm()
    
    context = {
        'title': 'Search', 
        'form' : form
    }

    return render(request, 'ticket_search/search.html', context)


def results(request):
    context = {
        'title': 'Results', 
    }

    return render(request, 'ticket_search/results.html', context)
