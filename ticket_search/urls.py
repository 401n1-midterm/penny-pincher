from django.urls import path

from .views import (about, check_results, delete_result, delete_search,
                    history, home, results, search, wait)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('search/', search, name='search'),
    path('delete_search/<int:search_id>/', delete_search, name='delete_search'),
    path('wait/', wait, name='wait'),
    path('results/', results, name='results'),
    path('delete_result/<int:result_id>/', delete_result, name='delete_result'),
    path('history/', history, name='history'),
    path('check_results/<int:search_id>/', check_results, name='check_results'),

]
