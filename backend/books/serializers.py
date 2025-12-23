from rest_framework import serializers
from .models import Book, Bookmark, AladinListItem

# 알라딘 API로부터 받아온 도서 목록 아이템
class AladinListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AladinListItem
        fields = [
            "id",
            "isbn13",
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
    customerReviewRank = serializers.SerializerMethodField()
    
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
            "customerReviewRank",
        ]
        
    def get_is_bookmarked(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return Bookmark.objects.filter(user=request.user, book=obj).exists()
    
    def get_customerReviewRank(self, obj):
        item = AladinListItem.objects.filter(isbn13=obj.isbn13).first()  # Meta.ordering=-id 적용
        if not item or item.customer_review_rank is None:
            return 0
        return int(item.customer_review_rank)

    

class BookSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "isbn13",
            "title",
            "author",
            "publisher",
            "pub_date",
            "cover",
            "sales_point",
            "category_name",
        ]