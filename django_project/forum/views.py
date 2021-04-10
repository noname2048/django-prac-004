# python built-in
import datetime
import logging

# django built-in
# base
from django.http.request import HttpRequest
from django.http.response import (
    HttpResponse,
    Http404,
    HttpResponseNotAllowed,
    HttpResponseNotModified,
)

# auth
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required

# db
from django.db.models.query_utils import Q
from django.db import transaction

# views
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.core.paginator import Paginator
from django.core import paginator
from django.contrib import messages

# apps
from forum import models as forum_models
from forum import forms as forum_forms

logger = logging.getLogger("django-server")


def post_list(request):
    """포스트 리스트를 리턴하는 뷰

    허용된 메소드: GET

    컨텍스트
    page_obj: built-in pagintor 객체
    page.previous_page_range: index list of previous page -3 (offset=3)
    page.next_page_range: index list of next page +3 (offset=3)
    totalcount: 전체 게시글 수

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
        return HttpResponseNotAllowed(request)


@login_required
def post_new(request):
    """새로운 포스트를 작성하는 뷰

    허용된 메소드
    GET - 포스트 작성 폼 리턴
    POST - 프스트 작성하고 작성된 게시글로 이동

    로그인이 필요합니다.

    게시글 작성시 ip와 author는 request에서 정보를 취득합니다.
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

            return redirect(resolve_url("forum:posts_detail", post.id))

    elif request.method == "GET":
        form = forum_forms.ForumPostForm()

        return render(
            request,
            "forum/post_new.html",
            {
                "form": form,
            },
        )

    else:
        return HttpResponseNotAllowed()


def post_detail(request: HttpRequest, pk: int):
    """게시글의 상세 내용을 보여주는 페이지

    허용되는 메소드: GET

    pk 가 없거나, is_active 가 false 이면 404를 띄웁니다.

    조회수를 위해 ip와 user는 조회수를 위해 자동으로 수집됩니다.
    만약 둘다 6시간내에 기록이 없다면 1 상승시킵니다.

    컨텍스트로는
    1. 카테고리 정보,
    2. 게시글 정보,
    3. 댓글 정보,
    4. 새로 만들 댓글 폼
    을 리턴합니다.
    """
    if request.method == "GET":

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
                hitcount = forum_models.ForumPostHitCount.objects.create(
                    post=post, user=user, ip=ip
                )
        else:
            try:
                forum_models.ForumPostHitCount.objects.get(
                    Q(post=post), Q(ip=ip), Q(date__gte=now_before6)
                )
            except forum_models.ForumPostHitCount.DoesNotExist:
                hitcount = forum_models.ForumPostHitCount.objects.create(post=post, ip=ip)

        category = post.category
        comments = post.forumcomment_set.filter(is_active=True)
        new_comment_form = forum_forms.ForumCommentForm(auto_id=False)

        return render(
            request,
            "forum/post_detail.html",
            {
                "category": category,
                "post": post,
                "comments": comments,
                "new_comment_form": new_comment_form,
            },
        )

    else:
        return HttpResponseNotAllowed()


def comments_new(request: HttpRequest, post_pk: int):
    """댓글작성을 하는 뷰.
    post에 comment 폼이 제공되므로 해당 뷰에서는 오로지 post만 받아 댓글을 작성하고, 뒤로가기를 합니다.

    허용된 메소드: POST
    """

    if request.method == "POST":
        # post_pk 와 is_active를 filter로 object를 가져옵니다.
        try:
            post = forum_models.ForumPost.objects.get(pk=post_pk, is_active=True)
        except forum_models.ForumPost.DoesNotExist:
            raise Http404("Post Not Exist")

        logger.warning("oh")

        form = forum_forms.ForumCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = get_user(request)
            comment.is_active = True

            with transaction.atomic():
                comment.save()

                post.cache_comments_count += 1
                post.save()
        else:
            messages.warning(request, "댓글 작성에서 문제가 있었습니다.")

        return redirect(
            resolve_url(
                "forum:posts_detail",
                post.id,
            )
        )

    else:
        return HttpResponseNotAllowed(request)


@login_required
def posts_likes(request: HttpRequest, post_pk: int):
    """게시글의 좋아요 구현
    좋아요 처리하고 나서는 뒤로가기

    혹시 좋아요를 낚시 링크에 달 수 도 있으니,
    추후에sms csrf token을 넣어 POST로 작성합니다.
    """

    if request.method in ["GET", "POST"]:
        try:
            post = forum_models.ForumPost.objects.get(pk=post_pk, is_active=True)
        except forum_models.ForumPost.DoesNotExist:
            return Http404("Post not exist.")

        user = get_user(request)
        forum_models.ForumLike.objects.create(post=post, author=user)

        # return HttpResponse(status=204)
        return redirect(resolve_url("forum:posts_detail", post_pk))
    else:
        return HttpResponseNotAllowed()


@login_required
def comments_likes(request: HttpRequest, post_pk: int, comment_pk: int):

    if request.method in ["GET", "POST"]:
        try:
            post = forum_models.ForumPost.objects.get(pk=post_pk, is_active=True)
        except forum_models.ForumPost.DoesNotExist:
            return Http404("Post not exist")

        try:
            comment = post.comments.get(pk=comment_pk)
        except forum_models.ForumComment.DoesNotExist:
            return Http404("Comments not exist")

        # TODO : 댓글 추가

    return HttpResponse(status=204)