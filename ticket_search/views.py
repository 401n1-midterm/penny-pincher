import time

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django_q.tasks import async_task

from .forms import SearchQueryForm
from .models import SearchQuery


TEMP_DATA = (None, None)


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
                return redirect('wait')

            except ValidationError as err:
                messages.error(request, err)

    else:
        form = SearchQueryForm()

    context = {
        'title': 'Search',
        'form': form
    }

    return render(request, 'ticket_search/search.html', context)


def test(task):
    global TEMP_DATA
    TEMP_DATA = task.result
    print(TEMP_DATA)


def wait(request):
    """
    async_task('function to run (absolute path)',
               function arguments,
               hook - the function that is run after the job is finished')
    """
    async_task('ticket_search.functions.run_search',
               'Seattle', 'Minsk',
               hook='ticket_search.views.test')

    context = {
        'title': 'Wait',
    }

    return render(request, 'ticket_search/wait.html', context)


def results(request):
    global TEMP_DATA
    print(TEMP_DATA)

    departure_prices, arrival_prices = TEMP_DATA

    context = {
        'title': 'Results',
        'departure_prices': departure_prices,
        'arrival_prices': arrival_prices,
    }

    return render(request, 'ticket_search/results.html', context)
