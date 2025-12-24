from rest_framework import serializers
from .models import Board, Prefix, Post, Comment


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
    user_profile_image = serializers.SerializerMethodField()
    prefix_name = serializers.CharField(source="prefix.name", read_only=True)

    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "user_id", "user_nickname", "user_profile_image",
            "prefix_name", "title", "content",
            "liked",                 
            "like_count", "comment_count",
            "created_at", "updated_at",
        ]

    def get_user_nickname(self, obj):
        return _nickname(obj.user)

    def get_user_profile_image(self, obj):
        return _profile_image(obj.user, self.context.get("request"))

    def get_liked(self, obj):
        return _liked(obj.id, self.context)


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
        return (value or "").strip()


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_nickname = serializers.SerializerMethodField()
    user_profile_image = serializers.SerializerMethodField()
    parent_comment_id = serializers.IntegerField(source="parent_comment.id", read_only=True)

    like_count = serializers.IntegerField(read_only=True)
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id", "user_id", "user_nickname", "user_profile_image",
            "parent_comment_id",
            "content",
            "liked",       
            "like_count",
            "created_at",
        ]

    def get_user_nickname(self, obj):
        return _nickname(obj.user)

    def get_user_profile_image(self, obj):
        return _profile_image(obj.user, self.context.get("request"))

    def get_liked(self, obj):
        return _liked(obj.id, self.context) 


class CommentWriteSerializer(serializers.Serializer):
    content = serializers.CharField()
    parent_comment_id = serializers.IntegerField(required=False)

    def validate_content(self, value):
        v = (value or "").strip()
        if not v:
            raise serializers.ValidationError("content is required.")
        return v
