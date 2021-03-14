from django.forms import forms
from . import models as account_models
from django.contrib.auth import forms as auth_forms


class SignupForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = account_models.User
        fields = ["username", "email", "first_name", "last_name"]
