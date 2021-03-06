from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, resolve_url, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from . import forms as accounts_forms
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.utils.http import url_has_allowed_host_and_scheme
import logging

logger = logging.getLogger("django.server")
# login_view = LoginView.as_view(template_name="accounts/login.html")


class AccountLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_field_name = "next"

    # def get_redirect_url(self) -> str:
    #     next_url = self.request.META.get("HTTP_REFERER", None)
    #     if next_url:
    #         if next_url == resolve_url("accounts:login"):
    #             return redirect(resolve_url("index"))

    #         url_is_safe = url_has_allowed_host_and_scheme(
    #             url=next_url,
    #             allowed_hosts=self.get_success_url_allowed_hosts(),
    #             require_https=self.request.is_secure(),
    #         )

    #         return next_url if url_is_safe else super().get_redirect_url()
    #     else:
    #         return super().get_redirect_url()


login_view2 = AccountLoginView.as_view()


def login_view(request):
    if request.method == "GET":

        if request.user.is_authenticated:
            next = request.GET.get("next", None)
            if next:
                return redirect(next)
            else:
                next = request.META.get("HTTP_REFERER", "None")

                if next:
                    return redirect(next)

                else:
                    return redirect(resolve_url("index"))
        else:
            form = AuthenticationForm()
            next = request.GET.get("next", None)

            return render(
                request,
                "accounts/login.html",
                {
                    "form": form,
                    "next": next,
                },
            )

    if request.method == "POST":
        # messages.info(request, "aaaa")
        # logger.info("aaaa")

        if request.user.is_authenticated:
            return redirect(resolve_url("index"))

        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = authenticate(
                request, username=form.get_user(), password=request.POST.get("password")
            )
            auth_login(request, user)

            next_url = request.META.get("HTTP_REFERER", None)
            if next_url == resolve_url("accounts:login"):
                return redirect(resolve_url("index"))
            else:
                return redirect(next_url)

        else:
            return render(
                request,
                "accounts/login.html",
                {
                    "form": form,
                },
            )


def logout_view(request):

    if request.user.is_anonymous:
        messages.info(request, "로그아웃 상태입니다.")
    else:
        auth_logout(request)
        messages.success(request, "성공적으로 로그아웃 하였습니다.")

    next_url = request.META.get("HTTP_REFERER", None)
    if next_url:
        return redirect(next_url)
    else:
        return redirect(resolve_url("index"))


def signup_view(request):

    if request.method == "POST":

        form = accounts_forms.SignupForm(request.POST)
        if form.is_valid():

            signup_user = form.save(commit=False)
            auth_login(request, signup_user)

            referer = request.META.get("HTTP_REFERER", None)
            if referer:
                next_url = referer
            else:
                next = request.GET.get("next", None)
                if next:
                    next_url = next
                else:
                    next_url = resolve_url("root")
            return redirect(next_url)

        else:
            form = accounts_forms.SignupForm(request.POST)
        return render(
            request,
            "accounts/signup.html",
            {
                "form": form,
            },
        )

    if request.method == "GET":
        form = accounts_forms.SignupForm()
    return render(
        request,
        "accounts/signup.html",
        {
            "form": form,
        },
    )


def findpass(request):

    if request.method == "GET":
        form = FindPassForm()

        return render(
            request,
            "accounts/findpass.html",
            {
                "form": form,
            },
        )