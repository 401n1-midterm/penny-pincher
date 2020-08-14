web: gunicorn penny_pincher.wsgi:application --preload --workers 8 --log-level debug
worker: python manage.py qcluster
