import datetime

from crispy_forms.layout import Field
from django import forms

from .models import SearchQuery


# Create the form class.
class SearchQueryForm(forms.ModelForm):
    date_from = forms.DateField(initial=datetime.date.today)
    date_to = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = SearchQuery
        exclude = ['user', 'date_created']
