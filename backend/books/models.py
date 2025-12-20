from django.db import models
from django.conf import settings

# Create your models here.
class Bestsellers(models.Model):

    # 알라딘 카테고리 정보 (보존용)
    category_id = models.IntegerField()
    category_name = models.CharField(max_length=255)

    # 상품 타입
    mall_type = models.CharField(max_length=20)

    # 알라딘 상품 식별자
    item_id = models.IntegerField(unique=True)

    # ISBN 정보
    isbn = models.CharField(max_length=20, blank=True, null=True)
    isbn13 = models.CharField(max_length=20, blank=True, null=True)

    # 기본 정보
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    publisher = models.CharField(max_length=255)
    pub_date = models.DateField()
    description = models.TextField(blank=True)
    cover = models.URLField()

    # 베스트셀러 지표
    best_rank = models.PositiveIntegerField()
    sales_point = models.PositiveIntegerField(default=0)
    customer_review_rank = models.PositiveSmallIntegerField(null=True)


class BestsellerSync(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    

class Book(models.Model):
    isbn13 = models.CharField(max_length=20, unique=True)

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    pub_date = models.DateField()
    description = models.TextField(blank=True)
    cover = models.URLField(blank=True)
    sales_point = models.IntegerField(null=True, blank=True)

    category_id = models.IntegerField(null=True, blank=True)
    category_name = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.isbn13})"



# 북마크
class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="bookmarked_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "book")