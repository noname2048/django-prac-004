from django.http.response import HttpResponseRedirect
from django.shortcuts import render, resolve_url, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from . import forms as accounts_forms
from django.contrib.auth import login as auth_login


login_view = LoginView.as_view(template_name="accounts/login.html")


def logout_view(request):

    if request.user.is_anonymous:
        messages.info(request, "로그아웃 상태입니다.")
    else:
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
