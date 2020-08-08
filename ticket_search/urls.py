from django.urls import path
from .views import about, home, search


urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('search/', search, name='search'),
]
