from rest_framework import serializers
from .models import Bestsellers, Book, Bookmark

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
    is_bookmarked = serializers.SerializerMethodField()
    
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
            "is_bookmarked",
        ]
        
    def get_is_bookmarked(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return Bookmark.objects.filter(user=request.user, book=obj).exists()