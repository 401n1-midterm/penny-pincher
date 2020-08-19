import datetime

from crispy_forms.layout import Field
from django import forms

from .models import SearchQuery


# Create the form class.
class SearchQueryForm(forms.ModelForm):

    # Disable autocomplete for date fields
    def __init__(self, *args, **kwargs):
        super(SearchQueryForm, self).__init__(*args, **kwargs)
        self.fields['date_from'].widget.attrs.update({
            'autocomplete': 'off',
            'onkeydown': 'return false',
        })
        self.fields['date_to'].widget.attrs.update({
            'autocomplete': 'off',
            'onkeydown': 'return false',
        })

    date_from = forms.DateField()
    date_to = forms.DateField()

    class Meta:
        model = SearchQuery
        exclude = ['user', 'date_created', 'error']
