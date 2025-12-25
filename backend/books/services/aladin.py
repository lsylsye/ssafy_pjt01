# books/services/aladin.py

import requests
from datetime import timedelta, datetime
from django.conf import settings
from django.utils import timezone
from books.models import Book
from books.models import AladinSync, AladinListItem

def _parse_iso_date(s: str):
    if not s:
        return None
    s = str(s).strip()
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except Exception:
        return None

def _to_cover500(url: str) -> str:
    if not url:
        return ""
    url = str(url)
    if "/cover500/" in url:
        return url
    return url.replace("/coversum/", "/cover500/")

def get_or_create_book_by_isbn13(isbn13: str) -> Book:
    book = Book.objects.filter(isbn13=isbn13).first()
    if book:
        return book

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

    book = Book.objects.create(
        isbn13=isbn13,
        title=item.get("title"),
        author=item.get("author"),
        publisher=item.get("publisher"),
        pub_date=_parse_iso_date(item.get("pubDate")),
        description=item.get("description", ""),
        cover=_to_cover500(item.get("cover", "")),
        category_id=item.get("categoryId"),
        category_name=item.get("categoryName", ""),
        sales_point=item.get("salesPoint", 0),
        customer_review_rank=item.get("customerReviewRank"),
    )

    return book


def is_aladin_fresh(query_type: str, ttl_hours: int = 24) -> bool:
    sync = AladinSync.objects.filter(query_type=query_type).first()
    if not sync:
        return False
    return timezone.now() - sync.updated_at < timedelta(hours=ttl_hours)


def touch_aladin_sync(query_type: str):
    AladinSync.objects.update_or_create(query_type=query_type)


def _fetch_itemlist_from_aladin(query_type: str, max_results: int = 10, start: int = 1):
    params = {
        "ttbkey": settings.ALADIN_TTB_KEY,
        "QueryType": query_type,
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
            "cover": _to_cover500(it.get("cover", "") or ""),
            "best_rank": it.get("bestRank"),
            "sales_point": it.get("salesPoint") or 0,
            "customer_review_rank": it.get("customerReviewRank"),
        }

        AladinListItem.objects.update_or_create(
            query_type=query_type,
            item_id=item_id,
            defaults=defaults,
        )

    AladinListItem.objects.filter(query_type=query_type).exclude(item_id__in=alive_item_ids).delete()
    touch_aladin_sync(query_type)


def get_cached_aladin_list(query_type: str, limit: int, ttl_hours: int = 24):
    if not is_aladin_fresh(query_type=query_type, ttl_hours=ttl_hours):
        refresh_aladin_list(query_type=query_type, max_results=limit)

    qs = AladinListItem.objects.filter(query_type=query_type)

    if query_type == "Bestseller":
        qs = qs.order_by("best_rank", "id")
    else:
        qs = qs.order_by("-pub_date", "-sales_point", "-id")

    return qs[:limit]


def search_books_by_query(query: str, max_results: int = 1):
    params = {
        "ttbkey": settings.ALADIN_TTB_KEY,
        "Query": query,
        "QueryType": "Keyword",
        "MaxResults": max_results,
        "start": 1,
        "SearchTarget": "Book",
        "Output": "JS",
        "Version": settings.ALADIN_API_VERSION,
    }

    try:
        res = requests.get(settings.ALADIN_SEARCH_URL, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        return data.get("item", [])
    except Exception as e:
        print(f"🚨 알라딘 검색 API 에러: {e}")
        return []
