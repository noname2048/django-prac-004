from .base import *

import os
from dotenv import load_dotenv

env_path = BASE_DIR.parent / ".env"
load_dotenv(dotenv_path=env_path)

DEBUG = True
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
# try:
#     import json
#     from django.core.exceptions import ImproperlyConfigured

#     SECRET_DIR = BASE_DIR.parent / ".secrets.json"
#     SECRET_KEY = json.load(open(SECRET_DIR))["DJANGO_SECRET_KEY"]
# except:
#     raise ImproperlyConfigured("[DEV] SECRET_KEY NOT FOUND! ")

ALLOWED_HOSTS = [
    "localhost",
]

INTERNAL_IPS = [
    "localhost",
]

DATABASES = {
    "default": {
        "NAME": "postgres",
        "ENGINE": "django.db.backends.postgresql",
        "USER": "postgres",
        "HOST": os.environ["PRODUCT_DB_POSTGRES_HOST"],
        "PASSWORD": os.environ["PRODUCT_DB_PASSWORD"],
        "PORT": 5432,
    },
}

# USE_DB = "default"
# USE_DB = "dev"
# USE_DB = "product"

# if USE_DB == "dev":
#     DATABASES.update(
#         {
#             "dev": {
#                 "NAME": "postgres",
#                 "ENGINE": "django.db.backends.postgresql",
#                 "USER": "postgres",
#                 "PASSWORD": "example",
#                 "HOST": "localhost",
#                 "PORT": 5431,
#             },
#         }
#     )

# if USE_DB == "product":
#     DATABASES.update(
#         {
#             "product": {
#                 "NAME": "postgres",
#                 "ENGINE": "django.db.backends.postgresql",
#                 "USER": os.getenv("PRODUCT_DB_USER"),
#                 "PASSWORD": os.getenv("PRODUCT_DB_PASSWORD"),
#                 "HOST": os.getenv("PRODUCT_DB_HOST"),
#                 "PORT": 5432,
#             },
#         }
#     )

# DATABASES.update(
#     {
#         "default": {
#             "NAME": "postgres",
#             "ENGINE": "django.db.backends.postgresql",
#             # "USER": "root",
#             "PASSWORD": os.getenv("PRODUCT_DB_PASSWORD"),
#             "HOST": os.getenv("PRODUCT_DB_HOST"),
#             "PORT": 5432,
#         },
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

AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
