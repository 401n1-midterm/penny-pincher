from django import forms

from .models import SearchQuery


# Create the form class.
class SearchQueryForm(forms.ModelForm):
     class Meta:
        model = SearchQuery
        exclude = ['date_created']
        