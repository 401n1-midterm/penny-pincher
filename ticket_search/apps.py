from django.apps import AppConfig
from django.core.management import call_command


class TicketSearchConfig(AppConfig):
    name = 'ticket_search'

    def ready(self):
        call_command('qcluster')
