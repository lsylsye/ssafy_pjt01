from django.db import models

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


class Book(models.Model):
    # 식별자 (기준 키)
    isbn13 = models.CharField(max_length=20, unique=True)

    # 기본 도서 정보
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    pub_date = models.DateField()
    description = models.TextField(blank=True)
    cover = models.URLField(blank=True)

    # 카테고리 (알라딘 기준)
    category_id = models.IntegerField(null=True, blank=True)
    category_name = models.CharField(max_length=255, blank=True)

    # 베스트셀러 정보 (해당되는 경우만)
    best_rank = models.PositiveIntegerField(null=True, blank=True)

    # 🤖 AI / Wikipedia 기반 작가 정보
    author_info = models.TextField(blank=True)
    author_works = models.JSONField(blank=True, null=True)
    author_image = models.URLField(blank=True)

    author_source = models.CharField(
        max_length=20,
        choices=[
            ("wiki", "Wikipedia"),
            ("ai", "AI"),
        ],
        default="ai",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.isbn13})"