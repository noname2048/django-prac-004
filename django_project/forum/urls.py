from django.urls import path, include
from django.views.generic import TemplateView
from . import views as forum_view

app_name = "forum"

urlpatterns = [
    path("", forum_view.post_list, name="main"),
    path("posts/", forum_view.post_list, name="posts_list"),
    path("posts/new/", forum_view.post_new, name="posts_new"),
    path("posts/<int:pk>/", forum_view.post_detail, name="posts_detail"),
    path("posts/<int:post_pk>/comments/new/", forum_view.comments_new, name="comments_new"),
]
