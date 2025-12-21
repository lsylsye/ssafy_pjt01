import random
import requests
from django.conf import settings
from django.db.models import Count

from books.models import Bookmark
from users.models import Follow 


def _norm_author(author_str: str) -> str:
    if not author_str:
        return ""
    s = str(author_str).strip()
    s = s.replace("(지은이)", "").replace("(저자)", "").replace("(옮긴이)", "").strip()
    if "," in s:
        s = s.split(",")[0].strip()
    return s


def _fetch_author_books_salespoint(author: str, max_results: int = 30):
    """
    알라딘 ItemSearch: QueryType=Author, Sort=SalesPoint
    """
    params = {
        "ttbkey": settings.ALADIN_TTB_KEY,
        "Query": author,
        "QueryType": "Author",
        "SearchTarget": "Book",
        "MaxResults": max_results,
        "start": 1,
        "Sort": "SalesPoint",
        "Output": "JS",
        "Version": settings.ALADIN_API_VERSION,
    }
    res = requests.get(settings.ALADIN_SEARCH_URL, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()
    return data.get("item", []) or []


def recommend_bookmark_based(user, need=5, recent_n=5, fetch_n=30):
    """
    북마크 기반:
    1) 사용자 최근 북마크 recent_n권 조회
    2) 그 안에서 '작가' 중복 제거 후 랜덤 1명 선택
    3) 해당 작가 인기책(SalesPoint) 목록에서 내 북마크 제외 후 5권 추천
    반환: Book이 아니라 "알라딘 item dict" 리스트
    """
    recent = (
        Bookmark.objects.filter(user=user)
        .select_related("book")
        .order_by("-created_at")[:recent_n]
    )
    if not recent:
        return []

    # 내 북마크 ISBN
    my_isbns = set(
        Bookmark.objects.filter(user=user).values_list("book__isbn13", flat=True)
    )

    # 최근 북마크에서 작가 후보 만들기(중복 제거)
    authors = []
    for bm in recent:
        a = _norm_author(getattr(bm.book, "author", ""))
        if a:
            authors.append(a)

    authors = list(set(authors))
    if not authors:
        return []

    picked_author = random.choice(authors)

    items = _fetch_author_books_salespoint(picked_author, max_results=fetch_n)

    # 내 북마크 제외 + 5권 채우기
    picked = []
    seen = set()
    for it in items:
        isbn13 = (it.get("isbn13") or "").strip()
        item_id = it.get("itemId")
        key = isbn13 or str(item_id)

        if not key or key in seen:
            continue
        seen.add(key)

        if isbn13 and isbn13 in my_isbns:
            continue

        picked.append(it)
        if len(picked) == need:
            break

    return picked


def recommend_follow_based(user, need=5, top_follow_limit=5, bookmark_pool=20):
    """
    팔로우 기반(최적화 버전):
    1) 내가 팔로우한 유저 중 bookmark_count >= need
    2) 팔로우 최신순으로 TOP top_follow_limit명(5명) 뽑기 (5명 미만이면 있는 만큼)
    3) 랜덤 셔플
    4) 셔플 순서대로 '그 유저 북마크 최신 bookmark_pool개 중 랜덤 need권' 추천
       - 내 북마크 ISBN 제외
       - need권 못 채우면 다음 후보로
    반환: Book 객체 리스트
    """
    my_isbns = set(
        Bookmark.objects.filter(user=user).values_list("book__isbn13", flat=True)
    )

    follows = (
        Follow.objects.filter(from_user=user)
        .annotate(bookmark_count=Count("to_user__bookmarks", distinct=True))
        .filter(bookmark_count__gte=need)
        .order_by("-created_at")[:top_follow_limit]
    )

    target_ids = [f.to_user_id for f in follows]
    if not target_ids:
        return []

    random.shuffle(target_ids)

    for uid in target_ids:
        qs = (
            Bookmark.objects.filter(user_id=uid)
            .exclude(book__isbn13__in=my_isbns)
            .select_related("book")
            .order_by("-created_at")[:bookmark_pool]
        )
        books = [bm.book for bm in qs]
        if len(books) < need:
            continue
        return random.sample(books, need)

    return []
