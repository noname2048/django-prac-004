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

# DATABASES.update(
#     {
#         "dev": {
#             "NAME": os.getenv("DJANGO_DB_NAME"),
#             "ENGINE": "django.db.backends.postgresql",
#             "USER": os.getenv("DJANGO_DB_USERNAME"),
#             "PASSWORD": os.getenv("DJANGO_DB_PASSWORD"),
#             "HOST": os.getenv("DJANGO_DB_HOST"),
#             "PORT": 5432,
#         }
#     }
# )

# DATABASE_ROUTERS = [
#     "account.routers.AccountRouter",
# ]

FIRST_USER = {
    "username": "noname2048",
    "email": "sungwook.csw@gmail.com",
    "password": "admin",
}

from dotenv import load_dotenv

env_path = BASE_DIR.parent / ".env"
load_dotenv(dotenv_path=env_path)

# DATABASES.update(
#     {
#         "default": {
#             "NAME": "postgres",
#             "ENGINE": "django.db.backends.postgresql",
#             "USER": os.getenv("PRODUCT_DB_USER"),
#             "PASSWORD": os.getenv("PRODUCT_DB_PASSWORD"),
#             "HOST": os.getenv("PRODUCT_DB_HOST"),
#             "PORT": 5432,
#         },
#     }
# )

# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
