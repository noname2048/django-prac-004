from django.core.management import BaseCommand, CommandParser
from django.conf import settings

from django.contrib.auth import get_user_model
from forum.models import ForumPost


class Command(BaseCommand):
    help = "renew cache in forumpost model"

    def handle(self, *args, **options):
        posts = ForumPost.objects.all()
        for post in posts:

            post.cache_comments_count = post.forumcomment_set.count()
            if post.category:
                post.category_name = post.category.name
            else:
                post.category_name = "없음"
            post.user_name = post.user.username
            post.cache_likes_count = post.forumlike_set.count()
            post.cache_views_count = post.forumposthitcount_set.count()

            post.save()
