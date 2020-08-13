from django.urls import path

from .views import about, home, results, search, wait

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('search/', search, name='search'),
    path('wait/', wait, name='wait'),
    path('results/', results, name='results'),

]
