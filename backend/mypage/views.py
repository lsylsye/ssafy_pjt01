# backend/mypage/views.py
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from books.models import Bookmark
from .serializers import MyBookmarkSerializer, MyProfileUpdateSerializer

from users.models import Follow
from grass.services import get_level_payload
from community.models import Post, Review, Comment
from django.contrib.contenttypes.models import ContentType


def _build_profile_response(request, user):
    followers_count = Follow.objects.filter(to_user=user).count()
    following_count = Follow.objects.filter(from_user=user).count()

    profile_image_url = ""
    if getattr(user, "profile_image", None) and user.profile_image:
        try:
            profile_image_url = request.build_absolute_uri(user.profile_image.url)
        except Exception:
            profile_image_url = user.profile_image.url

    level_payload = get_level_payload(user)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "nickname": getattr(user, "nickname", ""),
        "favorite_country": getattr(user, "favorite_country", None),
        "favorite_genre": getattr(user, "favorite_genre", None),
        "profile_image": profile_image_url,
        "followers_count": followers_count,
        "following_count": following_count,
        "exp_total": level_payload["exp_total"],
        "level": level_payload["level"],
        "level_progress": level_payload["level_progress"],
    }


# 내 정보 조회 + 수정(닉네임/선호국가/선호장르/프로필이미지)
@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def my_profile(request):
    user = request.user

    if request.method == "PATCH":
        serializer = MyProfileUpdateSerializer(
            user,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 저장 후 최신 값 다시 로드(이미지 url 등)
        user.refresh_from_db()

    return Response(_build_profile_response(request, user))


# 내 북마크 조회
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_bookmarks(request):
    qs = (
        Bookmark.objects
        .filter(user=request.user)
        .select_related("book")
        .order_by("-created_at")
    )
    serializer = MyBookmarkSerializer(qs, many=True)
    return Response(serializer.data)


# 내가 작성한 글 조회
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_posts(request):
    me = request.user

    posts = (
        Post.objects.filter(user=me)
        .select_related("board__community")
        .order_by("-created_at")
    )
    reviews = (
        Review.objects.filter(user=me)
        .select_related("board__community")
        .order_by("-created_at")
    )

    items = []

    for p in posts:
        country = (p.board.community.country or "").lower()
        items.append({
            "type": "FREE",
            "type_name": "자유",
            "title": p.title,
            "created_at": p.created_at,
            "country": country,
            "board_slug": "free",
            "detail_url": f"/api/community/{country}/free/{p.id}/",
        })

    for r in reviews:
        country = (r.board.community.country or "").lower()
        items.append({
            "type": "REVIEW",
            "type_name": "리뷰",
            "title": r.book_title,
            "created_at": r.created_at,
            "country": country,
            "board_slug": "review",
            "detail_url": f"/api/community/{country}/review/{r.id}/",
        })

    items.sort(key=lambda x: x["created_at"], reverse=True)
    return Response(items)


# 내가 작성한 댓글 조회
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_comments(request):
    me = request.user

    qs = (
        Comment.objects.filter(user=me)
        .select_related("content_type")
        .order_by("-created_at")
    )

    post_ct = ContentType.objects.get_for_model(Post)
    review_ct = ContentType.objects.get_for_model(Review)

    post_ids = [c.object_id for c in qs if c.content_type_id == post_ct.id]
    review_ids = [c.object_id for c in qs if c.content_type_id == review_ct.id]

    post_map = {
        p.id: p for p in Post.objects.filter(id__in=post_ids).select_related("board__community")
    }
    review_map = {
        r.id: r for r in Review.objects.filter(id__in=review_ids).select_related("board__community")
    }

    items = []
    for c in qs:
        if c.content_type_id == post_ct.id:
            p = post_map.get(c.object_id)
            if not p:
                items.append({
                    "comment_id": c.id,
                    "content": c.content,
                    "created_at": c.created_at,
                    "type": "",
                    "post_id": c.object_id,
                    "post_title": "삭제된 글",
                    "country": "",
                    "board_slug": "",
                    "detail_url": "",
                })
                continue

            country = (p.board.community.country or "").lower()
            board_slug = p.board.slug
            items.append({
                "comment_id": c.id,
                "content": c.content,
                "created_at": c.created_at,
                "type": "FREE",
                "post_id": p.id,
                "post_title": p.title,
                "country": country,
                "board_slug": board_slug,
                "detail_url": f"/community/{country}/{board_slug}/{p.id}",
            })

        elif c.content_type_id == review_ct.id:
            r = review_map.get(c.object_id)
            if not r:
                items.append({
                    "comment_id": c.id,
                    "content": c.content,
                    "created_at": c.created_at,
                    "type": "REVIEW",
                    "post_id": c.object_id,
                    "post_title": "삭제된 글",
                    "country": "",
                    "board_slug": "",
                    "detail_url": "",
                })
                continue

            country = (r.board.community.country or "").lower()
            board_slug = r.board.slug
            items.append({
                "comment_id": c.id,
                "content": c.content,
                "created_at": c.created_at,
                "type": "REVIEW",
                "post_id": r.id,
                "post_title": r.book_title,
                "country": country,
                "board_slug": board_slug,
                "detail_url": f"/community/{country}/{board_slug}/{r.id}",
            })

    return Response(items)
