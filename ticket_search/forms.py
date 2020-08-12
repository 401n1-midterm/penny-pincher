from crispy_forms.layout import Field
from django import forms

from .models import SearchQuery


# Create the form class.
class SearchQueryForm(forms.ModelForm):
    departure_city = Field('Departure City', css_class="black-fields")

    class Meta:
        model = SearchQuery
        exclude = ['date_created']
