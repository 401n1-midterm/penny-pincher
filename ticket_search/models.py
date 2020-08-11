from django.db import models


class SearchQuery(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    departure_city = models.CharField(max_length=128)
    arrival_city = models.CharField(max_length=128)
    date_from = models.DateField()
    date_to = models.DateField()
    stay_duration = models.IntegerField(null=True, blank=True)

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


  
