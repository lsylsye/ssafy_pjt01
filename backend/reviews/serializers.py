from rest_framework import serializers
from .models import Review

def _nickname(user):
    return getattr(user, "nickname", None) or getattr(user, "username", "")

def _profile_image(user, request):
    if not user.profile_image:
        return None
    url = user.profile_image.url
    if request:
        return request.build_absolute_uri(url)
    return url

def _liked(obj_id, context):
    liked_ids = context.get("liked_ids")
    if not liked_ids:
        return False
    return obj_id in liked_ids

class ReviewWriteSerializer(serializers.Serializer):
    book_title = serializers.CharField()
    book_author = serializers.CharField()
    content = serializers.CharField()

    rating = serializers.IntegerField(required=False, allow_null=True)

    isbn13 = serializers.CharField(required=False, allow_blank=True)
    publisher = serializers.CharField(required=False, allow_blank=True)
    pub_date = serializers.CharField(required=False, allow_blank=True)
    cover = serializers.CharField(required=False, allow_blank=True)

    def validate_book_title(self, value):
        v = (value or "").strip()
        if not v:
            raise serializers.ValidationError("book_title is required.")
        return v

    def validate_book_author(self, value):
        v = (value or "").strip()
        if not v:
            raise serializers.ValidationError("book_author is required.")
        return v

    def validate_content(self, value):
        v = (value or "").strip()
        if not v:
            raise serializers.ValidationError("content is required.")
        return v

    def validate_rating(self, value):
        if value is None:
            return value
        if value < 1 or value > 5:
            raise serializers.ValidationError("rating must be 1~5")
        return value

def _to_cover500(url: str) -> str:
    if not url: return ""
    return str(url).replace("/coversum/", "/cover500/")

class ReviewListSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_nickname = serializers.SerializerMethodField()
    user_profile_image = serializers.SerializerMethodField()

    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    liked = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id", "user_id", "user_nickname", "user_profile_image",
            "book_title", "book_author",
            "isbn13", "publisher", "pub_date", "cover",
            "rating", "content",
            "liked",                 
            "like_count", "comment_count",
            "created_at", "updated_at",
        ]

    def get_cover(self, obj):
        return _to_cover500(obj.cover)

    def get_user_nickname(self, obj):
        return _nickname(obj.user)

    def get_user_profile_image(self, obj):
        return _profile_image(obj.user, self.context.get("request"))

    def get_liked(self, obj):
        return _liked(obj.id, self.context)
