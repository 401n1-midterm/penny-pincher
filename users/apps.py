from django.apps import AppConfig
from django.core.management import call_command


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        call_command('qcluster')
