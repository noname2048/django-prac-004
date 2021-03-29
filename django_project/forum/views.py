from django.core import paginator
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from . import models as forum_models
from . import forms as forum_forms
from django import http
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def post_list(request):
    if request.method == "GET":

        forum_posts = forum_models.ForumPost.objects.all()
        paginator = Paginator(forum_posts, 25)
        page_number = int(request.GET.get("page", 1))
        page_obj = paginator.get_page(page_number)

        offset = 3
        page_obj.previous_page_range = range(max(1, page_number - offset), page_number)
        page_obj.next_page_range = range(
            page_number + 1, min(page_number + offset, len(paginator.page_range)) + 1
        )

        return render(
            request,
            "forum/main.html",
            {
                "page_obj": page_obj,
                "total_count": forum_posts.count(),
            },
        )

    else:
        return http.HttpResponseNotAllowed(request)


@login_required
def post_new(request):
    if request.method == "GET":
        form = forum_forms.ForumPostForm()

        return render(
            request,
            "forum/post_new.html",
            {
                "form": form,
            },
        )

    elif request.method == "POST":
        form = forum_forms.ForumPostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            post.author = get_user(request)
            post.ip = request.META["REMOTE_ADDR"]
            post.tags.add(*post.extract_tags(form.tag_help))

            post.save()

            return redirect(resolve_url("forum:post_list"))


import datetime


def post_detail(request, pk):
    post = get_object_or_404(forum_models.ForumPost, pk=pk)

    user = get_user(request)
    ip = request.META["REMOTE_ADDR"]
    now = datetime.datetime.now()
    now_before6 = now - datetime.timedelta(hours=6)

    if user.is_authenticated:
        try:
            forum_models.ForumPostHitCount.objects.get(
                Q(post=post), Q(ip=ip) | Q(user=user), Q(date__gte=now_before6)
            )
        except forum_models.ForumPostHitCount.DoesNotExist:
            hitcount = forum_models.ForumPostHitCount.objects.create(post=post, user=user, ip=ip)
    else:
        try:
            forum_models.ForumPostHitCount.objects.get(
                Q(post=post), Q(ip=ip), Q(date__gte=now_before6)
            )
        except forum_models.ForumPostHitCount.DoesNotExist:
            hitcount = forum_models.ForumPostHitCount.objects.create(post=post, ip=ip)

    return render(
        request,
        "forum/post_detail.html",
        {
            "post": post,
        },
    )
