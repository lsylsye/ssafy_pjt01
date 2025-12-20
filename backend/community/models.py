from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Community(models.Model):
    country = models.CharField(max_length=10, unique=True)  # KR/JP/CN/EN
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["country"]

    def __str__(self):
        return f"{self.country}-{self.name}"


class Board(models.Model):
    BOARD_TYPES = [
        ("FREE", "자유"),
        ("REVIEW", "리뷰"),
    ]

    community = models.ForeignKey("community.Community", on_delete=models.CASCADE, related_name="boards")
    slug = models.SlugField(max_length=50)  # free / review / ...
    name = models.CharField(max_length=50)
    board_type = models.CharField(max_length=20, choices=BOARD_TYPES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["community", "slug"], name="unique_board_per_community"),
        ]
        ordering = ["slug"]

    def __str__(self):
        return f"{self.community.country}-{self.slug}"


class Prefix(models.Model):
    board = models.ForeignKey("community.Board", on_delete=models.CASCADE, related_name="prefixes")
    name = models.CharField(max_length=30)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="created_prefixes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["board", "name"], name="unique_prefix_per_board"),
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.board.slug}:{self.name}"


class Post(models.Model):
    board = models.ForeignKey("community.Board", on_delete=models.CASCADE, related_name="posts")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    prefix = models.ForeignKey("community.Prefix", null=True, blank=True, on_delete=models.SET_NULL, related_name="posts")

    title = models.CharField(max_length=100)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.id}:{self.title}"


class Review(models.Model):
    board = models.ForeignKey("community.Board", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")

    # 필수 입력(도서명, 저자)
    book_title = models.CharField(max_length=200)
    book_author = models.CharField(max_length=200)
    content = models.TextField() 

    # 옵션1(검색 클릭 시 자동으로 넘어올 수 있는 메타)
    isbn13 = models.CharField(max_length=13, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    pub_date = models.CharField(max_length=20, blank=True)
    cover = models.URLField(blank=True)

    # 옵션2(리뷰 내용)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)  # 1~5

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")

    # Post/Review 공통 대상
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey("content_type", "object_id")

    # 대댓글
    parent_comment = models.ForeignKey(
        "self",
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="replies",
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")

    # Post/Review/Comment 공통 좋아요
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "content_type", "object_id"], name="unique_like_per_user_target"),
        ]
