from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage


class BaseTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ForumPost(BaseTimeModel):
    title = models.CharField(max_length=30)
    file = models.FileField(upload_to="files")
