from django.contrib import admin
from . import models as forum_models

admin.site.register(forum_models.ForumCategory)
admin.site.register(forum_models.ForumPost)
admin.site.register(forum_models.ForumTag)
admin.site.register(forum_models.ForumLike)
admin.site.register(forum_models.ForumComment)
