import requests
from datetime import timedelta, datetime
from django.conf import settings
from django.utils import timezone
from books.models import Book
from .models import AladinSync, AladinListItem

def _parse_iso_date(s: str):
    if not s:
        return None
    s = str(s).strip()
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except Exception:
        return None
    

def get_or_create_book_by_isbn13(isbn13: str) -> Book:

    # DB 먼저 확인
    book = Book.objects.filter(isbn13=isbn13).first()
    if book:
        return book

    # 알라딘 상품 조회
    params = {
        "ttbkey": settings.ALADIN_TTB_KEY,
        "ItemId": isbn13,
        "ItemIdType": "ISBN13",
        "Output": "JS",
        "Version": settings.ALADIN_API_VERSION,
    }

    res = requests.get(settings.ALADIN_LOOKUP_URL, params=params)
    res.raise_for_status()
    data = res.json()

    items = data.get("item", [])
    if not items:
        raise ValueError("해당 ISBN13의 도서를 찾을 수 없습니다.")

    item = items[0]

    # 3️⃣ Book 생성
    book = Book.objects.create(
        isbn13=isbn13,
        title=item.get("title"),
        author=item.get("author"),
        publisher=item.get("publisher"),
        pub_date=_parse_iso_date(item.get("pubDate")),
        description=item.get("description", ""),
        cover=item.get("cover", ""),
        category_id=item.get("categoryId"),
        category_name=item.get("categoryName", ""),
        sales_point=item.get("salesPoint", "")
    )

    return book


def is_aladin_fresh(query_type: str, ttl_hours: int = 24) -> bool:
    sync = AladinSync.objects.filter(query_type=query_type).first()
    if not sync:
        return False
    return timezone.now() - sync.updated_at < timedelta(hours=ttl_hours)


def touch_aladin_sync(query_type: str):
    """
    updated_at = auto_now=True 라서 update_or_create만 해도 갱신됨
    """
    AladinSync.objects.update_or_create(query_type=query_type)


def _fetch_itemlist_from_aladin(query_type: str, max_results: int = 10, start: int = 1):
    """
    알라딘 ItemList API 호출
    settings.ALADIN_ITEMLIST_URL 필요
    """
    params = {
        "ttbkey": settings.ALADIN_TTB_KEY,
        "QueryType": query_type,          # Bestseller / ItemNewSpecial / ...
        "MaxResults": max_results,
        "start": start,
        "SearchTarget": "Book",
        "Output": "JS",
        "Version": settings.ALADIN_API_VERSION,
    }

    res = requests.get(settings.ALADIN_ITEMLIST_URL, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()
    return data.get("item", [])


def refresh_aladin_list(query_type: str, max_results: int = 10):
    """
    - 알라딘에서 목록 받아와서 DB(AladinListItem)에 upsert
    - query_type별로 현재 살아있는 item_id만 남기고 나머지 삭제
    - sync 갱신
    """
    items = _fetch_itemlist_from_aladin(query_type=query_type, max_results=max_results, start=1)

    alive_item_ids = []
    for it in items:
        item_id = it.get("itemId")
        if not item_id:
            continue
        alive_item_ids.append(item_id)

        defaults = {
            "category_id": it.get("categoryId"),
            "category_name": it.get("categoryName", "") or "",
            "mall_type": it.get("mallType", "") or "",
            "isbn": it.get("isbn", "") or "",
            "isbn13": it.get("isbn13", "") or "",
            "title": it.get("title", "") or "",
            "author": it.get("author", "") or "",
            "publisher": it.get("publisher", "") or "",
            "pub_date": _parse_iso_date(it.get("pubDate")),
            "description": it.get("description", "") or "",
            "cover": it.get("cover", "") or "",
            "best_rank": it.get("bestRank"),  # 없을 수 있음
            "sales_point": it.get("salesPoint") or 0,
            "customer_review_rank": it.get("customerReviewRank"),
        }

        AladinListItem.objects.update_or_create(
            query_type=query_type,
            item_id=item_id,
            defaults=defaults,
        )

    # query_type별 DB 정리(현재 받아온 것만 유지)
    AladinListItem.objects.filter(query_type=query_type).exclude(item_id__in=alive_item_ids).delete()

    # sync touch
    touch_aladin_sync(query_type)


def get_cached_aladin_list(query_type: str, limit: int, ttl_hours: int = 24):
    """
    - TTL 내면 DB에서 그대로
    - TTL 지났으면 refresh 후 DB에서 반환
    """
    if not is_aladin_fresh(query_type=query_type, ttl_hours=ttl_hours):
        refresh_aladin_list(query_type=query_type, max_results=limit)

    qs = AladinListItem.objects.filter(query_type=query_type)

    # 정렬: 베스트셀러는 best_rank 기준, 나머지는 최신/판매지표 기준
    if query_type == "Bestseller":
        qs = qs.order_by("best_rank", "id")
    else:
        qs = qs.order_by("-pub_date", "-sales_point", "-id")

    return qs[:limit]