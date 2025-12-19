import requests
from django.conf import settings
from books.models import Book


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
        pub_date=item.get("pubDate"),
        description=item.get("description", ""),
        cover=item.get("cover", ""),
        category_id=item.get("categoryId"),
        category_name=item.get("categoryName", ""),
    )

    return book
