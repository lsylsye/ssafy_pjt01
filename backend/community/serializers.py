from rest_framework import serializers
from .models import Community, Board, Prefix, Post, Review, Comment

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["slug", "name", "board_type"]


class PrefixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prefix
        fields = ["id", "name"]
        read_only_fields = ["id"]


class PostSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_nickname = serializers.CharField(source="user.nickname", read_only=True)
    prefix_name = serializers.CharField(source="prefix.name", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user_id",
            "user_nickname",
            "prefix_name",
            "title",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user_id", "user_nickname", "prefix_name", "created_at", "updated_at"]


# POST 생성용: prefix를 문자열로 입력받기 위해 분리
class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()
    prefix = serializers.CharField(max_length=30, required=False, allow_blank=True)


class ReviewSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_nickname = serializers.CharField(source="user.nickname", read_only=True)
    isbn13 = serializers.CharField(source="book.isbn13", read_only=True)
    book_title = serializers.CharField(source="book.title", read_only=True)
    sales_point = serializers.IntegerField(source="book.sales_point", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user_id",
            "user_nickname",
            "isbn13",
            "book_title",
            "sales_point",
            "rating",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user_id", "user_nickname", "isbn13", "book_title", "sales_point", "created_at", "updated_at"]


class ReviewCreateSerializer(serializers.Serializer):
    isbn13 = serializers.CharField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    content = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_nickname = serializers.CharField(source="user.nickname", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user_id", "user_nickname", "content", "created_at"]
        read_only_fields = ["id", "user_id", "user_nickname", "created_at"]
