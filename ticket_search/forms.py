from django.forms import ModelForm
from .models import SearchQuery

# Create the form class.
class SearchQueryForm(ModelForm):
     class Meta:
        model = SearchQuery
        exclude = ['date_created']
