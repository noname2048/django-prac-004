from django.contrib import admin
from . import models as forum_models


admin.site.register(forum_models.ForumPost)
