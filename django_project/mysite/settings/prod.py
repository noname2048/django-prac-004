from .base import *
import os
from django.core.exceptions import ImproperlyConfigured
import json

DEBUG = False
SECRET_DIR = BASE_DIR.parent / ".secrets.json"

try:
    secrets = json.load(open(SECRET_DIR))
    SECRET_KEY = secrets["DJANGO_SECRET_KEY"]
    ALLOWED_HOSTS = secrets["ALLOWED_HOSTS"]
except:
    raise ImproperlyConfigured("[DEV] SECRET_KEY NOT FOUND! ")
