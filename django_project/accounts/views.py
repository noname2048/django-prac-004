from django.http.response import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.contrib.auth.views import LoginView
from django.contrib import messages

login_view = LoginView.as_view(template_name="accounts/login.html")


def logout_view(request):

    if request.user.is_anonymous:
        messages.info(request, "로그아웃 상태입니다.")
    else:
        messages.success(request, "성공적으로 로그아웃 하였습니다.")

    back = request.META.get("HTTP_REFERER", None)
    if back:
        return HttpResponseRedirect(back)
    else:
        return HttpResponseRedirect(resolve_url("root"))
