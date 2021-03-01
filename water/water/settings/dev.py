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

import os

DATABASES.update(
    {
        "default": {
            "NAME": os.getenv("DJANGO_DB_NAME"),
            "ENGINE": "django.db.backends.postgresql",
            "USER": os.getenv("DJANGO_DB_USERNAME"),
            "PASSWORD": os.getenv("DJANGO_DB_PASSWORD"),
            "HOST": os.getenv("DJANGO_DB_HOST"),
            "PORT": 5432,
        }
    }
)

# DATABASES_ROUTERS = [
#    "forum.routers.MultiDBRouter",
# ]

FIRST_USER = {
    "username": "noname2048",
    "email": "sungwook.csw@gmail.com",
    "password": "admin",
}