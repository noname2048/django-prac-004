from django.urls import path, include
from . import views as account_view

app_name = "accounts"

urlpatterns = [
    path("login/", account_view.login_view, name="login"),
    path("logout/", account_view.logout_view, name="logout"),
    path("signup/", account_view.signup_view, name="signup"),
    path("findpass/", account_view.findpass, name="findpass")
]
