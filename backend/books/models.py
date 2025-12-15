from django.db import models

# Create your models here.
class Bestsellers(models.Model):
    category = models.IntegerField()

    # 알라딘 원본 카테고리 정보 (보존용)
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

