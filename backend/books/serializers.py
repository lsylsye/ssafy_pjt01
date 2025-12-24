from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Bookmark, AladinListItem
from reviews.models import Review
from .services.aladin import _to_cover500

User = get_user_model()

# 알라딘 API로부터 받아온 도서 목록 아이템
class AladinListItemSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()
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
        
    def get_cover(self, obj):
        return _to_cover500(obj.cover)


# 하위 시리얼라이저: 리뷰 (도서 상세 페이지용)
class BookReviewSerializer(serializers.ModelSerializer):
    user_nickname = serializers.SerializerMethodField()
    user_profile_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = [
            "id",
            "user_nickname",
            "user_profile_image",
            "content",
            "rating",
            "created_at",
        ]
        
    def get_user_nickname(self, obj):
        return getattr(obj.user, "nickname", None) or obj.user.username

    def get_user_profile_image(self, obj):
        if obj.user.profile_image:
            return obj.user.profile_image.url
        return None  # Or default path if you prefer


# 알라딘 API로부터 받아온 도서 목록 아이템
# 도서 상세 페이지
class BookDetailSerializer(serializers.ModelSerializer):
    is_bookmarked = serializers.SerializerMethodField()
    customerReviewRank = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    
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
            "reviews",
            "review_count",
        ]
        
    def get_cover(self, obj):
        return _to_cover500(obj.cover)

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

    def get_reviews(self, obj):
        # 해당 도서의 리뷰 (최신순)
        # obj: Book model instance
        qs = Review.objects.filter(isbn13=obj.isbn13).order_by("-id")
        return BookReviewSerializer(qs, many=True).data

    def get_review_count(self, obj):
        return Review.objects.filter(isbn13=obj.isbn13).count()

    

class BookSimpleSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()

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

    def get_cover(self, obj):
        return _to_cover500(obj.cover)