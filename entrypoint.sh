#!/bin/sh

echo "[MIGRATE]"
python manage.py migrate --no-input
python manage.py migrate --database=dev --no-input
python manage.py inituser
python manage.py collectstatic --no-input
# python manage.py runserver 0:8000
# gunicorn water.wsgi:application --bind 0.0.0.0:8000
