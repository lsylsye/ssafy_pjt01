# books/services_bestsellers.py
import requests
from django.conf import settings
from django.utils.dateparse import parse_date

from .models import Bestsellers, BestsellerSync


def refresh_bestsellers_from_aladin(max_results=10):
    params = {
        "ttbkey": settings.ALADIN_TTB_KEY,
        "QueryType": "Bestseller",
        "MaxResults": max_results,
        "start": 1,
        "SearchTarget": "Book",
        "Output": "JS",
        "Version": settings.ALADIN_API_VERSION,
    }

    res = requests.get(settings.ALADIN_ITEMLIST_URL, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()

    items = data.get("item", []) or []
    if not items:
        raise ValueError("알라딘 베스트셀러 응답이 비어있습니다.")

    alive_item_ids = []

    for idx, item in enumerate(items, start=1):
        item_id = item.get("itemId")
        if not item_id:
            continue
        alive_item_ids.append(item_id)

        pub_date_str = item.get("pubDate")  # "YYYY-MM-DD"
        pub_date = parse_date(pub_date_str) if pub_date_str else None
        if pub_date is None:
            raise ValueError(f"pubDate 파싱 실패: {pub_date_str}")

        Bestsellers.objects.update_or_create(
            item_id=item_id,
            defaults={
                "category_id": item.get("categoryId") or 0,
                "category_name": item.get("categoryName") or "",
                "mall_type": item.get("mallType") or "BOOK",
                "isbn": item.get("isbn"),
                "isbn13": item.get("isbn13"),
                "title": item.get("title") or "",
                "author": item.get("author") or "",
                "publisher": item.get("publisher") or "",
                "pub_date": pub_date,
                "description": item.get("description") or "",
                "cover": item.get("cover") or "",
                "best_rank": item.get("bestRank") or idx,  # 없으면 idx
                "sales_point": item.get("salesPoint") or 0,
                "customer_review_rank": item.get("customerReviewRank"),
            },
        )

    # DB에서 더 이상 존재하지 않는 항목 삭제
    Bestsellers.objects.exclude(item_id__in=alive_item_ids).delete()
    
    # 마지막 갱신시각 업데이트
    BestsellerSync.objects.update_or_create(id=1, defaults={})

    return True
