from django.contrib import admin
from . import models as forum_models

admin.site.register(forum_models.ForumCategory)
# admin.site.register(forum_models.ForumPost)
@admin.register(forum_models.ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "category", "author", "ip"]

    actions = ["change_category"]

    def change_category(self, request, queryset):
        category = forum_models.ForumCategory.objects.filter(name="general").first()
        queryset.update(category=category)

    change_category.short_description = "선택한 포스트의 카테고리를 변경"


admin.site.register(forum_models.ForumTag)
admin.site.register(forum_models.ForumLike)
admin.site.register(forum_models.ForumComment)


@admin.register(forum_models.ForumPostHitCount)
class ForumPostHitCountAdmin(admin.ModelAdmin):
    list_display = ["id", "date", "post", "ip", "user"]


admin.site.register(forum_models.ForumPostIPRecord)
admin.site.register(forum_models.ForumCommentIPRecord)
