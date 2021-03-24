from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

USER_MODLE = settings.AUTH_USER_MODEL


class BaseTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ForumCategory(BaseTimeModel):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)


class ForumPost(BaseTimeModel):
    author = models.ForeignKey(USER_MODLE, on_delete=models.CASCADE)

    title = models.CharField(max_length=30)
    content = models.TextField(max_length=500)  # max length effect only wigets
    file = models.FileField(upload_to="files")
    ip = models.GenericIPAddressField(null=True, editable=False)

    delete = models.BooleanField(default=False)


class ForumTag(BaseTimeModel):
    name = models.CharField(max_length=50, unique=True)


class ForumComment(BaseTimeModel):
    author = models.ForeignKey(USER_MODLE, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    delete = models.BooleanField(default=False)


class ForumLike(BaseTimeModel):
    author = models.ForeignKey(USER_MODLE, on_delete=models.CASCADE)

    # forum = models.ManytoOn
