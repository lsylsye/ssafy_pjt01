import random
import requests
from django.conf import settings
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from users.models import Follow
from books.models import Book, Bookmark, AladinSync, AladinListItem


def _is_fresh(key: str, ttl_hours: int = 24) -> bool:
    sync = AladinSync.objects.filter(query_type=key).first()
    if not sync:
        return False
    return timezone.now() - sync.updated_at < timedelta(hours=ttl_hours)


def _touch(key: str):
    AladinSync.objects.update_or_create(query_type=key)


def _fetch_itemsearch_author_sales(author: str, max_results: int = 20, start: int = 1):
    params = {
        "ttbkey": settings.ALADIN_TTB_KEY,
        "Query": author,
        "QueryType": "Author",        # 핵심
        "SearchTarget": "Book",
        "Sort": "SalesPoint",         # 판매지표 정렬
        "MaxResults": max_results,
        "Start": start,
        "Output": "JS",
        "Version": settings.ALADIN_API_VERSION,
    }
    res = requests.get(settings.ALADIN_SEARCH_URL, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()
    return data.get("item", [])


def _get_cached_author_sales(author: str, limit: int = 20, ttl_hours: int = 24):
    key = f"AuthorSales:{author}"

    if not _is_fresh(key, ttl_hours=ttl_hours):
        items = _fetch_itemsearch_author_sales(author, max_results=limit, start=1)

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
                "pub_date": None,  # 필요하면 기존 _parse_iso_date 써도 됨
                "description": it.get("description", "") or "",
                "cover": it.get("cover", "") or "",
                "best_rank": it.get("bestRank"),
                "sales_point": it.get("salesPoint") or 0,
                "customer_review_rank": it.get("customerReviewRank"),
            }

            AladinListItem.objects.update_or_create(
                query_type=key,
                item_id=item_id,
                defaults=defaults,
            )

        AladinListItem.objects.filter(query_type=key).exclude(item_id__in=alive_item_ids).delete()
        _touch(key)

    return AladinListItem.objects.filter(query_type=key).order_by("-sales_point", "-id")[:limit]


def recommend_bookmark_based_aladin(user, limit=5):
    recent = list(
        Bookmark.objects.filter(user=user)
        .select_related("book")
        .order_by("-created_at")[:5]
    )
    if not recent:
        return {"picked_author": None, "items": []}

    picked = random.choice(recent).book
    author = (picked.author or "").strip()
    if not author:
        return {"picked_author": None, "items": []}

    # 이미 북마크한 isbn13 제외
    bookmarked_isbn13 = set(
        Bookmark.objects.filter(user=user)
        .select_related("book")
        .values_list("book__isbn13", flat=True)
    )

    # 알라딘(캐시)에서 author 인기책 가져오기
    cand = _get_cached_author_sales(author, limit=30, ttl_hours=24)

    items = []
    for it in cand:
        if not it.isbn13:
            continue
        if it.isbn13 in bookmarked_isbn13:
            continue
        items.append(it)
        if len(items) == limit:
            break

    # 5권 못 채우면 빈 배열 정책 유지(너 설계대로)
    if len(items) != limit:
        return {"picked_author": author, "items": []}

    return {"picked_author": author, "items": items}


def recommend_follow_based(user, limit=5, pool_limit=5):
    candidates = (
        Follow.objects
        .filter(from_user=user)
        .values("to_user_id")
        .annotate(bookmark_count=Count("to_user__bookmarks"))  # related_name 맞아야 함
        .filter(bookmark_count__gte=limit)
        .order_by("-bookmark_count")[:pool_limit]
    )

    candidate_ids = [c["to_user_id"] for c in candidates]
    if not candidate_ids:
        return {"type": "follow_based", "picked_user_id": None, "items": []}

    picked_user_id = random.choice(candidate_ids)

    my_book_ids = Bookmark.objects.filter(user=user).values_list("book_id", flat=True)

    picked_bookmarks = (
        Bookmark.objects
        .filter(user_id=picked_user_id)
        .exclude(book_id__in=my_book_ids)
        .select_related("book")
        .order_by("-created_at")[:limit]
    )

    return {
        "type": "follow_based",
        "picked_user_id": picked_user_id,
        "items": [bm.book for bm in picked_bookmarks],
    }