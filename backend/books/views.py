import requests
from datetime import timedelta
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Bestsellers, Book, Bookmark, BestsellerSync
from .serializers import BestsellerSerializer, BookDetailSerializer
from .services import get_or_create_book_by_isbn13
from .services_bestsellers import refresh_bestsellers_from_aladin


# 베스트셀러 TOP10
@api_view(["GET"])
def bestseller_list(request):
    max_results = 10
    ttl = timedelta(hours=24)

    sync = BestsellerSync.objects.filter(id=1).first()
    qs = Bestsellers.objects.all().order_by("best_rank")[:max_results]

    is_fresh = False
    if sync and qs.count() >= max_results:
        is_fresh = (timezone.now() - sync.updated_at) <= ttl

    if not is_fresh:
        try:
            refresh_bestsellers_from_aladin(max_results=max_results)
            qs = Bestsellers.objects.all().order_by("best_rank")[:max_results]
        except Exception:
            # 알라딘 실패해도 DB 캐시가 있으면 캐시로 반환(서비스 안정성)
            if qs.exists():
                return Response(BestsellerSerializer(qs, many=True).data)
            return Response({"error": "bestsellers refresh failed"}, status=503)

    return Response(BestsellerSerializer(qs, many=True).data)

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



# 내 북마크 목록
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_bookmarks(request):
    bookmarks = (
        Bookmark.objects
        .filter(user=request.user)
        .select_related("book")
        .order_by("-created_at")
    )

    data = [
        {
            "isbn13": b.book.isbn13,
            "title": b.book.title,
            "author": b.book.author,
            "publisher": b.book.publisher,
            "pub_date": b.book.pub_date,
            "cover": b.book.cover,
            "bookmarked_at": b.created_at,
        }
        for b in bookmarks
    ]

    return Response(data)