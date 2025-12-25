# backend/mypage/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from books.models import Bookmark

User = get_user_model()


class MyBookmarkSerializer(serializers.ModelSerializer):
    isbn13 = serializers.CharField(source="book.isbn13")
    title = serializers.CharField(source="book.title")
    author = serializers.CharField(source="book.author")
    publisher = serializers.CharField(source="book.publisher")
    cover = serializers.URLField(source="book.cover")

    class Meta:
        model = Bookmark
        fields = [
            "isbn13",
            "title",
            "author",
            "publisher",
            "cover",
        ]


class MyProfileUpdateSerializer(serializers.ModelSerializer):
    """
    마이페이지에서 수정 허용할 필드만:
    - nickname
    - favorite_country
    - favorite_genre
    - profile_image
    """
    class Meta:
        model = User
        fields = ["nickname", "bio", "favorite_country", "other_country", "favorite_genre", "profile_image"]

    def validate_nickname(self, value):
        value = (value or "").strip()
        if not value:
            raise serializers.ValidationError("닉네임은 비어 있을 수 없습니다.")

        user = self.context["request"].user
        if User.objects.filter(nickname=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value
