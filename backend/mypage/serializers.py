# mypage/serializers.py
from rest_framework import serializers
from books.models import Bookmark


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
