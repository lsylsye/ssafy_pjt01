from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

class Review(models.Model):
    board = models.ForeignKey("community.Board", on_delete=models.CASCADE, related_name="reviews_list")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="book_reviews")

    book_title = models.CharField(max_length=200)
    book_author = models.CharField(max_length=200)
    content = models.TextField()

    isbn13 = models.CharField(max_length=13, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    pub_date = models.CharField(max_length=20, blank=True)
    cover = models.URLField(blank=True)

    rating = models.PositiveSmallIntegerField(null=True, blank=True)  # 1~5
    is_representative = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    comments_list = GenericRelation("community.Comment")
    likes_list = GenericRelation("community.Like")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.id}:{self.book_title}"
