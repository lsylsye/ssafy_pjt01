import requests
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, Bookmark
from .serializers import BookDetailSerializer, AladinListItemSerializer, BookSimpleSerializer
from .services import get_or_create_book_by_isbn13, get_cached_aladin_list
from .services.recommendations import recommend_bookmark_based_aladin, recommend_follow_based


# 베스트셀러 TOP10
@api_view(["GET"])
def bestseller_list(request):
    qs = get_cached_aladin_list(query_type="Bestseller", limit=10, ttl_hours=24)
    return Response(AladinListItemSerializer(qs, many=True).data)


# 주목할만한 신간
@api_view(["GET"])
def new_special_list(request):
    qs = get_cached_aladin_list("ItemNewSpecial", limit=5, ttl_hours=24)
    return Response(AladinListItemSerializer(qs, many=True).data)


# 도서 검색
@api_view(["GET"])
def book_search(request):
    q = request.GET.get("q")
    if not q:
        return Response({"error": "q parameter is required"}, status=400)

    query_type = request.GET.get("type", "Keyword")
    page = int(request.GET.get("page", 1))
    size = int(request.GET.get("size", 10))
    sort = request.GET.get("sort", "Accuracy")
    category_id = request.GET.get("category", 0)
    
    params = {
        "ttbkey": settings.ALADIN_TTB_KEY,
        "Query": q,
        "QueryType": query_type,
        "SearchTarget": "Book",
        "Start": page,
        "MaxResults": min(size, 50),
        "Sort": sort,
        "CategoryId": category_id,
        "Output": "JS",
        "Version": settings.ALADIN_API_VERSION,
    }

    res = requests.get(settings.ALADIN_SEARCH_URL, params=params)
    res.raise_for_status()
    data = res.json()
    
    items = []
    for item in data.get("item", []):
        items.append({
            "title": item.get("title"),
            "author": item.get("author"),
            "publisher": item.get("publisher"),
            "pub_date": item.get("pubDate"),
            "isbn13": item.get("isbn13"),
            "cover": item.get("cover"),
            "sales_point": item.get("salesPoint"),
            "customer_review_rank": item.get("customerReviewRank"),
        })

    return Response({
        "total": data.get("totalResults"),
        "page": page,
        "size": size,
        "items": items,
    })
    
    
    
# 도서 상세 페이지
@api_view(["GET"])
def book_detail(request, isbn13):
    try:
        book = get_or_create_book_by_isbn13(isbn13)
    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = BookDetailSerializer(book, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


# 북마크
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def bookmark_toggle(request, isbn13):
    user = request.user

    # Book 확보 (없으면 알라딘 → DB 저장)
    book = get_or_create_book_by_isbn13(isbn13)

    # 북마크 존재 여부 확인
    bookmark = Bookmark.objects.filter(user=user, book=book).first()

    if bookmark:
        # 이미 있으면 → 삭제
        bookmark.delete()
        return Response({
            "bookmarked": False,
            "created": False
        })

    # 없으면 → 생성
    Bookmark.objects.create(user=user, book=book)
    return Response({
        "bookmarked": True,
        "created": True
    })



# 책 추천 알고리즘
class RecommendBookmarkBasedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = recommend_bookmark_based_aladin(request.user, limit=5)
        return Response({
            "type": "bookmark_based",
            "picked_author": data["picked_author"],
            "items": AladinListItemSerializer(data["items"], many=True).data,
        })


class RecommendFollowBasedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = recommend_follow_based(request.user, limit=5, pool_limit=5)
        items = BookSimpleSerializer(data["items"], many=True).data
        return Response({
            "type": "follow_based",
            "picked_user_id": data["picked_user_id"],
            "items": items,
        })


class RecommendDebugView(APIView):
    """
    한 번에 둘 다 확인용
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        b = recommend_bookmark_based(request.user, limit=5)
        f = recommend_follow_based(request.user, limit=5, pool_limit=5)

        return Response({
            "bookmark_based": {
                "picked_author": b["picked_author"],
                "items": BookSimpleSerializer(b["items"], many=True).data,
            },
            "follow_based": {
                "picked_user_id": f["picked_user_id"],
                "items": BookSimpleSerializer(f["items"], many=True).data,
            },
        })