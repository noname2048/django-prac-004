from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from . import models as forum_models
from . import forms as forum_forms
from django import http
from django.contrib.auth.decorators import login_required


def post_list(request):
    if request.method == "GET":
        forum_posts = forum_models.ForumPost.objects.all()

        return render(
            request,
            "forum/main.html",
            {
                "forum_posts": forum_posts,
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
            post.author = request.user
            post.ip = request.META["REMOTE_ADDR"]
            post.save()

            return redirect(resolve_url("forum:post_list"))


def post_detail(request, pk):
    post = get_object_or_404(forum_models.ForumPost, pk=pk)

    return render(
        request,
        "forum/post_detail.html",
        {
            "post": post,
        },
    )
