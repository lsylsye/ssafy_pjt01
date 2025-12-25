from django.db import models
from django.conf import settings

# Create your models here.

class AladinSync(models.Model):
    query_type = models.CharField(max_length=50, unique=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.query_type} @ {self.updated_at}"


class AladinListItem(models.Model):
    query_type = models.CharField(max_length=50) 
    item_id = models.IntegerField()

    category_id = models.IntegerField(null=True, blank=True)
    category_name = models.CharField(max_length=255, blank=True)

    mall_type = models.CharField(max_length=20, blank=True)

    isbn = models.CharField(max_length=20, blank=True)
    isbn13 = models.CharField(max_length=20, blank=True)

    title = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    pub_date = models.DateField(null=True, blank=True)

    description = models.TextField(blank=True)
    cover = models.URLField(blank=True)

    best_rank = models.IntegerField(null=True, blank=True)  # Bestseller만 주로 씀
    sales_point = models.IntegerField(default=0)
    customer_review_rank = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["query_type", "item_id"], name="uniq_querytype_itemid")
        ]
        ordering = ["-id"]

    def __str__(self):
        return f"{self.query_type}:{self.title}({self.item_id})"


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
    customer_review_rank = models.IntegerField(null=True, blank=True)

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