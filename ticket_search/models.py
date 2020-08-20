from django.contrib.auth.models import User
from django.db import models


class SearchQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    departure_city = models.CharField(
        max_length=128, help_text='Your current city')
    arrival_city = models.CharField(
        max_length=128, help_text='City of your destination')
    date_from = models.DateField(help_text='First day of your availabilty')
    date_to = models.DateField(help_text='Last day of your availabilty')
    stay_duration = models.IntegerField(
        null=True, blank=True, help_text='*You will be given results &#177; 3 days from this number')
    error = models.CharField(default='', max_length=512)

    class Meta:
        ordering = ['date_created']

    @property
    def has_results(self):
        return len(self.result_set.all()) > 0

    @property
    def has_errors(self):
        return self.error != ''

    @property
    def get_results(self):
        return self.result_set.all()

    @property
    def get_result_count(self):
        return len(self.result_set.all())

    @property
    def get_price(self):
        if self.has_results:
            return self.result_set.first().price
        else:
            return 0.00

    def __str__(self):
        return f'{self.date_created}-{self.departure_city}-{self.arrival_city}'


class Result(models.Model):
    search_query = models.ForeignKey(SearchQuery, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    departure_city = models.CharField(max_length=128)
    arrival_city = models.CharField(max_length=128)
    date_from = models.DateField()
    date_to = models.DateField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.date_created}-{self.departure_city}-{self.arrival_city}-${self.price}'

    @property
    def get_duration(self):
        try:
            duration = int(str(self.date_to - self.date_from).split(' ')[0])
        except ValueError as err:
            duration = 0

        return duration
