web: gunicorn penny_pincher.wsgi:application --preload --workers 1 --log-level debug
worker: python manage.py qcluster
