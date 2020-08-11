import time

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from .forms import SearchQueryForm
from .functions import get_condor
from .models import SearchQuery


def home(request):

    context = {
        'title': 'Home',
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
        form = SearchQueryForm(request.POST)
        for error in form.errors:
            messages.error(request, error)

        if form.is_valid():
            departure_city = request.POST.get('departure_city')
            arrival_city = request.POST.get('arrival_city')
            date_from = request.POST.get('date_from')
            date_to = request.POST.get('date_to')
            stay_duration = request.POST['stay_duration'] if request.POST['stay_duration'] else None

            try:
                new_search = SearchQuery(
                    departure_city=departure_city,
                    arrival_city=arrival_city,
                    date_from=date_from,
                    date_to=date_to,
                    stay_duration=stay_duration,
                )
                new_search.save()
                return redirect('results')

            except ValidationError as err:
                messages.error(request, err)

    else:
        form = SearchQueryForm()

    context = {
        'title': 'Search',
        'form': form
    }

    return render(request, 'ticket_search/search.html', context)


def results(request):

    page_title = get_condor()

    context = {
        'title': 'Results',
        'page_title': page_title

    }

    return render(request, 'ticket_search/results.html', context)
