from django.core import paginator
from django.db.models.query_utils import Q
from django.http.response import Http404
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from . import models as forum_models
from . import forms as forum_forms
from django import http
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def post_list(request):
    """포스트 리스트를 리턴하는 뷰

    주요 컨텍스트로는 page_obj 와 totalcount 가 있습니다.
    page_obj 에는 기본적인 장고의 pagination 외에도
    previous_page_range, next_page_range 로 페이징을 추가 처리합니다.

    totalcount는 전체 게시글의 수를 나타냅니다.
    오로지 GET 방식으로만 받는 중입니다.
    """

    if request.method == "GET":

        q = request.GET.get("q")
        if q:

            forum_posts = forum_models.ForumPost.objects.filter(is_active=True).filter(
                title__icontains=q
            )
        else:
            forum_posts = forum_models.ForumPost.objects.filter(is_active=True)

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
    """새로운 포스트를 작성하는 뷰

    당연히 로그인이 필요합니다.
    GET 은 단순히 Form 을 이용하여 리턴합니다.

    POST의 경우에는 author와 ip는 자동으로 설정하는 항목입니다.
    """

    if request.method == "POST":
        form = forum_forms.ForumPostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            post.author = get_user(request)
            post.ip = request.META["REMOTE_ADDR"]
            post.save()

            tag_list = form.data.get("tag_help")
            tags = post.extract_tags(tag_list)

            if tags:
                post.tags.add(*tags)

            return redirect(resolve_url("forum:post_detail", post.id))

    elif request.method == "GET":
        form = forum_forms.ForumPostForm()

        return render(
            request,
            "forum/post_new.html",
            {
                "form": form,
            },
        )


import datetime


def post_detail(request, pk):
    """게시글을 보여주는 페이지

    pk가 있는데 게시글이 없다면 404를 보여줍니다.
    is_active 가 false 여도 404를 보여줍니다.

    ip와 user는 조회수를 위해 자동으로 수집됩니다.
    만약 둘다 6시간내에 기록이 없다면 조회수를 상승합니다.

    컨텍스트로는
    1. 카테고리 정보,
    2. 게시글 정보,
    3. 댓글 정보,
    4. 댓글 폼
    을 리턴합니다.
    """
    post = get_object_or_404(forum_models.ForumPost, pk=pk)
    if post.is_active == False:
        return Http404("Post does not exist")

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

    category = post.category
    comments = post.forumcomment_set.filter(is_active=True)

    return render(
        request,
        "forum/post_detail.html",
        {
            "category": category,
            "post": post,
            "comments": comments,
        },
    )
