from django.db import models
from django.db.models.deletion import CASCADE, SET_DEFAULT
from django.db.models.fields.related import ForeignKey
from django.utils import tree
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

USER_MODLE = settings.AUTH_USER_MODEL


class BaseTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ForumCategory(BaseTimeModel):
    name = models.CharField(unique=True, max_length=30)
    description = models.CharField(max_length=30)

    parent_category = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    # TODO: history for char fields

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class ForumTag(BaseTimeModel):
    name = models.CharField(unique=True, max_length=50)

    parent_tag = ForeignKey("self", null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name} (태그)"


class ForumPost(BaseTimeModel):
    author = models.ForeignKey(USER_MODLE, on_delete=models.CASCADE)
    category = models.ForeignKey(ForumCategory, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(ForumTag)

    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=30)
    content = models.TextField(max_length=500)  # max length effect only wigets
    file = models.FileField(upload_to="files")
    ip = models.GenericIPAddressField(null=True, editable=False)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class ForumLike(BaseTimeModel):
    author = models.ForeignKey(USER_MODLE, on_delete=models.CASCADE)
    posts = models.ForeignKey(ForumPost, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.author.username} likes {self.posts.title}"


class ForumComment(BaseTimeModel):
    author = models.ForeignKey(USER_MODLE, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=CASCADE)

    content = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.author.username}의 덧글: {self.content}"
