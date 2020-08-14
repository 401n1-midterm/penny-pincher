from django.urls import path

from .views import about, check_results, home, results, search, wait

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('search/', search, name='search'),
    path('wait/', wait, name='wait'),
    path('results/', results, name='results'),
    path('check_results/<int:search_id>/', check_results, name='check_results')

]
