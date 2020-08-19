import time
from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render


from .forms import SearchQueryForm
from .functions import get_cheapest_flights
from .models import Result, SearchQuery

from background_task import background
from .functions import run_search
from django.utils import timezone


def home(request):

    context = {
        'title': 'Home',
    }

    return render(request, 'ticket_search/home.html', context)


def about(request):

    context = {
        'title': 'About'
    }

    return render(request, 'ticket_search/about.html', context)


@login_required
def search(request):

    if request.method == 'POST':
        form = SearchQueryForm(request.POST)
        for error in form.errors:
            messages.error(request, 'Form submission failed, please try again')

        if form.is_valid():
            user = request.user
            departure_city = request.POST.get('departure_city')
            arrival_city = request.POST.get('arrival_city')
            date_from = request.POST.get('date_from')
            date_to = request.POST.get('date_to')
            stay_duration = request.POST['stay_duration'] if request.POST['stay_duration'] else None

            try:
                new_search = SearchQuery(
                    user=user,
                    departure_city=departure_city,
                    arrival_city=arrival_city,
                    date_from=date_from,
                    date_to=date_to,
                    stay_duration=stay_duration,
                )
                new_search.save()

                request.session['from_search_page'] = True
                request.session['search_id'] = new_search.pk

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


@background(schedule=timezone.now())
def process_data(search_query_id):
    function_return = run_search(search_query_id)
    search_query = SearchQuery.objects.get(pk=search_query_id)
    error_message = function_return.get('message', False)
    if error_message:
        search_query.error = error_message
        search_query.save()

    # Data process goes in here

    try:
        cheapest_flights = get_cheapest_flights(function_return, search_query)

        for flight in cheapest_flights:

            result = Result(
                search_query=search_query,
                departure_city=flight['departure_city'],
                arrival_city=flight['arrival_city'],
                date_from=flight['date_from'],
                date_to=flight['date_to'],
                price=flight['price']
            )

            result.save()

    except Exception as err:
        print(err)


def wait(request):

    # Check if the user is coming from the search page
    from_search_page = request.session.get('from_search_page', False)
    if from_search_page:

        # Remove the key so that the user can't refresh the page
        del request.session['from_search_page']

        search_id = request.session.get('search_id')
        request.session['from_wait_page'] = True

        # Call Selenium script async
        process_data(search_id)

        context = {
            'title':        'Wait',
            'search_id':    search_id,
        }

        return render(request, 'ticket_search/wait.html', context)

    else:
        return redirect('search')


def results(request):

    # Check if the user is coming from the wait page
    from_wait_page = request.session.get('from_wait_page', False)
    if from_wait_page:

        # Remove the key so that the user can't refresh the page
        del request.session['from_wait_page']

        search_id = request.session.get('search_id')
        search_query = SearchQuery.objects.get(pk=search_id)
        results = search_query.result_set.all()

        context = {
            'title': 'Results',
            'results': results
        }

        return render(request, 'ticket_search/results.html', context)
    else:
        return redirect('search')


def check_results(request, search_id):
    search_query = SearchQuery.objects.get(pk=search_id)

    return JsonResponse({'ready':           search_query.has_results,
                         'has_errors':      search_query.has_errors,
                         'error_message':   search_query.error})


@login_required
def history(request):
    user = request.user
    search_queries = user.searchquery_set.all()

    context = {
        'title':    'History',
        'search_queries':  search_queries
    }

    return render(request, 'ticket_search/history.html', context)


@login_required
def delete_result(request, result_id):
    try:
        result = Result.objects.get(pk=result_id)
        search_query = result.search_query
        result.delete()

        if not search_query.has_results:
            search_query.delete()

        messages.success(request, 'Result succesfully deleted')
    except Exception as err:
        messages.error(request, 'Can\'t delete the result!', err)

    return redirect('history')


@login_required
def delete_search(request, search_id):
    try:
        search_query = SearchQuery.objects.get(pk=search_id)
        search_query.delete()
        messages.success(request, 'Search sucefully deleted')
    except Exception as err:
        messages.error(request, 'Can\'t delete the search!', err)
    return redirect('history')
