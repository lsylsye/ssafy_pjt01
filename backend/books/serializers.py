from rest_framework import serializers
from .models import Bestsellers, Book

# 베스트셀러
class BestsellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bestsellers
        fields = [
            "id",
            "category_name",
            "title",
            "author",
            "publisher",
            "cover",
            "best_rank",
            "sales_point",
            "customer_review_rank",
        ]

# 도서 상세 페이지
class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "isbn13",
            "title",
            "author",
            "publisher",
            "pub_date",
            "description",
            "cover",
            "category_id",
            "category_name",
            "best_rank",
            "author_info",
            "author_works",
            "author_image",
            "author_source",
        ]