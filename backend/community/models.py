from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Community(models.Model):
    country = models.CharField(max_length=10, unique=True)   # KR/JP/CN/EN (확장 가능)
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
        ("NOTICE", "공지"),
        ("QNA", "질문"),
        ("SPOILER", "스포일러"),
    ]

    community = models.ForeignKey("community.Community", on_delete=models.CASCADE, related_name="boards")
    slug = models.SlugField(max_length=50)         # free / review / notice ...
    name = models.CharField(max_length=50)         # 자유게시판 / 리뷰게시판 ...
    board_type = models.CharField(max_length=20, choices=BOARD_TYPES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["community", "slug"], name="unique_board_per_community"),
        ]
        ordering = ["slug"]

    def __str__(self):
        return f"{self.community.country}-{self.slug}"


# 자유게시판 말머리
class Prefix(models.Model):
    board = models.ForeignKey("community.Board", on_delete=models.CASCADE, related_name="prefixes")
    name = models.CharField(max_length=30)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name="created_prefixes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["board", "name"], name="unique_prefix_per_board"),
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.board.slug}:{self.name}"


# 자유게시글
class Post(models.Model):
    board = models.ForeignKey("community.Board", on_delete=models.CASCADE, related_name="posts")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    prefix = models.ForeignKey("community.Prefix", null=True, blank=True,
                               on_delete=models.SET_NULL, related_name="posts")

    title = models.CharField(max_length=100)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.id}:{self.title}"


# 리뷰 (리뷰게시판 전용)
class Review(models.Model):
    board = models.ForeignKey("community.Board", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")

    # books 앱의 Book 모델 사용 (isbn13 캐시 구조)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE, related_name="reviews")

    rating = models.PositiveSmallIntegerField()  # 1~5
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(fields=["user", "book", "board"], name="unique_review_per_user_book_board"),
        ]

    def __str__(self):
        return f"{self.id}:{self.user_id}-{self.book_id}"


# 댓글: Post/Review 모두 달 수 있게 GenericRelation 사용
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()

    # Generic FK
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}:{self.user_id}"
