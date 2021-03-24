from django.urls import path, include
from django.views.generic import TemplateView
from . import views as forum_view

app_name = "forum"

urlpatterns = [
    path("", forum_view.post_list, name="main"),
    path("posts/", forum_view.post_list, name="post_list"),
    path("post/new/", forum_view.post_new, name="post_new"),
    path("post/<int:pk>/", forum_view.post_detail, name="post_detail"),
]
