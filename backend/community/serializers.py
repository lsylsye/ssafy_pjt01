from rest_framework import serializers
from .models import Board, Prefix, Post, Review, Comment


def _nickname(user):
    # users 모델에 nickname이 있다고 가정. 없으면 username fallback
    return getattr(user, "nickname", None) or getattr(user, "username", "")


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["slug", "name", "board_type"]


class PrefixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prefix
        fields = ["id", "name"]


class PostListSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_nickname = serializers.SerializerMethodField()
    prefix_name = serializers.CharField(source="prefix.name", read_only=True)

    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "user_id", "user_nickname",
            "prefix_name", "title", "content",
            "like_count", "comment_count",
            "created_at", "updated_at",
        ]

    def get_user_nickname(self, obj):
        return _nickname(obj.user)


class PostWriteSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    prefix = serializers.CharField(required=False, allow_blank=True)

    def validate_title(self, value):
        v = (value or "").strip()
        if not v:
            raise serializers.ValidationError("This field may not be blank.")
        return v

    def validate_content(self, value):
        v = (value or "").strip()
        if not v:
            raise serializers.ValidationError("This field may not be blank.")
        return v

    def validate_prefix(self, value):
        # prefix는 옵션: 공백이면 ""로 통일
        return (value or "").strip()


class ReviewWriteSerializer(serializers.Serializer):
    book_title = serializers.CharField()
    book_author = serializers.CharField()
    content = serializers.CharField()
    rating = serializers.IntegerField(required=False, allow_null=True) # 옵션(1~5)

    # 검색 클릭 시 자동으로 넘어올 수 있는 메타(옵션)
    isbn13 = serializers.CharField(required=False, allow_blank=True)
    publisher = serializers.CharField(required=False, allow_blank=True)
    pub_date = serializers.CharField(required=False, allow_blank=True)
    cover = serializers.CharField(required=False, allow_blank=True)

    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("content is required.")
        return value

    def validate_rating(self, value):
        if value is None:
            return value
        if value < 1 or value > 5:
            raise serializers.ValidationError("rating must be 1~5")
        return value



class ReviewListSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_nickname = serializers.SerializerMethodField()

    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id", "user_id", "user_nickname",
            "book_title", "book_author",
            "isbn13", "publisher", "pub_date", "cover",
            "rating", "content",
            "like_count", "comment_count",
            "created_at", "updated_at",
        ]

    def get_user_nickname(self, obj):
        return _nickname(obj.user)


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_nickname = serializers.SerializerMethodField()
    parent_comment_id = serializers.IntegerField(source="parent_comment.id", read_only=True)
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user_id", "user_nickname", "parent_comment_id", "content", "like_count", "created_at"]

    def get_user_nickname(self, obj):
        return _nickname(obj.user)


class CommentWriteSerializer(serializers.Serializer):
    content = serializers.CharField()
    parent_comment_id = serializers.IntegerField(required=False)
