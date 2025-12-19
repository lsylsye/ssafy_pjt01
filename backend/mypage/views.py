# mypage/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from books.models import Bookmark
from .serializers import MyBookmarkSerializer


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
