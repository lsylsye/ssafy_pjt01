# mypage/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from books.models import Bookmark
from .serializers import MyBookmarkSerializer

from users.models import Follow

# 내 정보 조회
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_profile(request):
    user = request.user
    
    followers_count = Follow.objects.filter(to_user=user).count()
    following_count = Follow.objects.filter(from_user=user).count()
    
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "nickname": getattr(user, "nickname", ""),
        "favorite_country": getattr(user, "favorite_country", None),
        "favorite_genre": getattr(user, "favorite_genre", None),
        "followers_count": followers_count,
        "following_count": following_count,
    })


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
