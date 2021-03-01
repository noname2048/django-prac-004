from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # username
    # first_name
    # last_name
    # email
    # is_staff
    # is_active
    # date_joined
    # objects

    class GenderInGender(models.TextChoices):
        MALE = "M", "남"
        FEMAILE = "F", "여"
