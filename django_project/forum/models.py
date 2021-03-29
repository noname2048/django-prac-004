from django.db import models
from django.db.models.deletion import CASCADE, SET_DEFAULT
from django.db.models.fields.related import ForeignKey
from django.utils import tree
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
import re

USER_MODLE = settings.AUTH_USER_MODEL


class BaseTimeModel(models.Model):
    """대부분의 모델에 사용되는 생성시간과 수정시간
    Meta 속성에 abstract을 선언하여 따로 생성되는 것을 막습니다.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ForumCategory(BaseTimeModel):
    """계층형 카테고리 (자기자신을 부모로 가지는) 자유게시판은 free, 일반 포럼은 general
    부모카테고리를 없에면 자식 카테고리는 부모를 null 로 가집니다.
    카테고리가 계층을 가지는 이유는 게시판을 세분화 하기 위함
    parent_category.name + " " + name 이 unique 하도록 차후에 변경
    """

    parent_category = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    name = models.CharField(unique=True, max_length=30)
    description = models.CharField(max_length=30)

    class Meta:
        """카테고리는 생성된 순서 오름차순으로 정렬 (general, free, ...)"""

        ordering = ["id"]

    def __str__(self):
        return self.name


class ForumTag(BaseTimeModel):
    """계층형 태그, 태그에 트리 관계가 있습니다.
    태그에 트리 관계가 있는 이유는 오타나 관련있는 태그를 한데 모으기 위함.
    게시글 모델에서 인풋에 따라 자동으로 생성하도록 합니다.
    """

    parent_tag = ForeignKey("self", null=True, on_delete=models.SET_NULL)
    name = models.CharField(unique=True, max_length=50)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name} (태그)"


class ForumPost(BaseTimeModel):
    """일반적인 게시판의 게시글 모델
    카테고리가 비어있으면 자동으로 free 로 지정합니다.
    삭제 대신 is_active를 사용하여 내용을 남기고, 삭제된것처럼 행동합니다.
    게시글 작성/수정에 사용된 ip를 남길 수 있도록 해야함
    """

    author = models.ForeignKey(USER_MODLE, on_delete=models.CASCADE)
    category = models.ForeignKey(ForumCategory, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(ForumTag)

    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=30)
    content = models.TextField(max_length=500)  # max length effect only wigets
    file = models.FileField(upload_to="files")
    ip = models.GenericIPAddressField(null=True, editable=False)

    class Meta:
        """가장 최근에 생성된 게시물이 앞으로 오게끔"""

        ordering = ["-id"]

    def __str__(self):
        return self.title

    def extract_tags(self, tag_list_str):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", tag_list_str)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = ForumTag.objects.get_or_create(name=tag_name)
        tag_list.append(tag)

        return tag_list


class ForumPostHitCount(models.Model):
    """조회수를 기록하기 위한 모델
    조건 1. 한개의 IP는 동일 게시글에 대하해 6시간당 조회수 1증가 가능
    조건 2. 한명의 유저는 동일 게시글에 대해 6시간당 조회수 1증가 가능
    효과 1. 여러대의 IP를 써도 로그인 했으면 조회수가 안올라감
    효과 2. 여러명의 유저를 동일 IP에서 사용해도 조회수가 안올라감
    """

    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    user = models.ForeignKey(USER_MODLE, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class ForumLike(BaseTimeModel):
    """게시글의 좋아요 기능 구현
    게시글과 사용자를 기록
    분석도 할 수 있도록 시간도
    """

    posts = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    author = models.ForeignKey(USER_MODLE, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """게시글의 좋아요는 가장 최근부터 내림차순으로"""

        ordering = ["-id"]

    def __str__(self):
        return f"{self.author.username} likes {self.posts.title}"


class ForumComment(BaseTimeModel):
    """덧글구현
    유투브 덧글처럼 덧글아래에 또다른 덧글을 한단계 까지만 허용
    삭제 대신 is_active 필드 활용
    """

    post = models.ForeignKey(ForumPost, on_delete=CASCADE)
    author = models.ForeignKey(USER_MODLE, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey("self", null=True, on_delete=models.CASCADE)

    content = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False)

    class Meta:
        """덧글은 먼저 쓴 사람부터 보이게"""

        ordering = ["id"]

    def __str__(self):
        return f"{self.author.username}의 덧글: {self.content}"


class ForumPostIPRecord(models.Model):
    """게시글에 대한 작성/수정 IP 기록을 남기기 위한 모델"""

    post = models.ForeignKey(ForumPost, on_delete=CASCADE)
    user = models.ForeignKey(USER_MODLE, on_delete=CASCADE)
    ip = models.GenericIPAddressField()
    date = models.DateTimeField(auto_now_add=True)


class ForumCommentIPRecord(models.Model):
    """덧글에 대한 작성/수정 IP 기록을 남기기 위한 모델"""

    comment = models.ForeignKey(ForumComment, on_delete=CASCADE)
    user = models.ForeignKey(USER_MODLE, on_delete=CASCADE)
    ip = models.GenericIPAddressField()
    date = models.DateTimeField(auto_now_add=True)
