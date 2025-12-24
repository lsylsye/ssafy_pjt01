# backend/community/models.py

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Board(models.Model):
    BOARD_TYPES = [
        ("FREE", "자유"),
        ("REVIEW", "리뷰"),
    ]

    slug = models.SlugField(max_length=50, unique=True)  # free / review / ...
    name = models.CharField(max_length=50)
    board_type = models.CharField(max_length=20, choices=BOARD_TYPES)

    class Meta:
        ordering = ["slug"]

    def __str__(self):
        return f"{self.slug}"


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

    book_title = models.CharField(max_length=200)
    book_author = models.CharField(max_length=200)
    content = models.TextField()

    isbn13 = models.CharField(max_length=13, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    pub_date = models.CharField(max_length=20, blank=True)
    cover = models.URLField(blank=True)

    rating = models.PositiveSmallIntegerField(null=True, blank=True)  # 1~5

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey("content_type", "object_id")

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

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "content_type", "object_id"], name="unique_like_per_user_target"),
        ]
