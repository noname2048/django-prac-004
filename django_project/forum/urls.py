from django.urls import path, include
from django.views.generic import TemplateView
from . import views as forum_view

app_name = "forum"

urlpatterns = [
    # 메인 리스트
    path("", forum_view.post_list, name="main"),
    # 리스트
    path("posts/", forum_view.post_list, name="posts_list"),
    # 게시글 새로쓰기
    path("posts/new/", forum_view.post_new, name="posts_new"),
    # 게시글 세부내역
    path("posts/<int:pk>/", forum_view.post_detail, name="posts_detail"),
    # 댓글 처리하기
    path("posts/<int:post_pk>/comments/new/", forum_view.comments_new, name="comments_new"),
    # 게시글 좋아요
    path("posts/<int:post_pk>/likes/", forum_view.posts_like, name="posts_like"),
    # 덧글 좋아요
    path(
        "posts/<int:post_pk>/comments/<int:comment_pk>/likes/",
        forum_view.comments_like,
        name="comments_like",
    ),
    # 덧글에 덧글쓰기
    path(
        "posts/<int:post_pk>/comments/<int:comment_pk>/new",
        forum_view.comment_comments,
        name="comments_comment",
    ),
]
