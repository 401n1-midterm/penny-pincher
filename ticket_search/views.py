import time
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django_q.tasks import async_task

from .forms import SearchQueryForm
from .models import Result, SearchQuery


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


def process_data(task):

    function_return = task.result
    search_query = SearchQuery.objects.get(pk=function_return['search_id'])

    error_message = function_return.get('message', False)
    if error_message:
        search_query.error = error_message
        search_query.save()

    print('process data', function_return)

    # Data process goes in here

    try:
        departure_city = search_query.departure_city
        arrival_city = search_query.arrival_city
        date_from = function_return['departure_prices'][0].get('date', '')
        date_to = function_return['arrival_prices'][0].get('date', '')
        price = Decimal(function_return['departure_prices'][0].get('price', '').split(' ')[1]) + \
            Decimal(function_return['arrival_prices']
                    [0].get('price', '').split(' ')[1])

        result = Result(
            search_query=search_query,
            departure_city=departure_city,
            arrival_city=arrival_city,
            date_from=date_from,
            date_to=date_to,
            price=price
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

        """
        async_task('function to run (absolute path)',
                function arguments,
                hook - the function that is run after the job is finished')
        """
        async_task('ticket_search.functions.run_search',
                   search_id,
                   hook='ticket_search.views.process_data')

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
