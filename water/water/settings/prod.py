from .base import *

DEBUG = False

try:
    import os
    from django.core.exceptions import ImproperlyConfigured

    SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
except:
    raise ImproperlyConfigured("[DEV] SECRET_KEY NOT FOUND! ")

ALLOWED_HOSTS = [
    "0.0.0.0",
    "www.noname2048.dev",
]
