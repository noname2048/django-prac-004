from .base import *

DEBUG = True

try:
    import json
    from django.core.exceptions import ImproperlyConfigured

    SECRET_DIR = BASE_DIR.parent / ".secrets.json"
    SECRET_KEY = json.load(open(SECRET_DIR))["DJANGO_SECRET_KEY"]
except:
    raise ImproperlyConfigured("[DEV] SECRET_KEY NOT FOUND! ")

ALLOWED_HOSTS = [
    "localhost",
]

INTERNAL_IPS = [
    "localhost",
]
