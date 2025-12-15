import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Bestsellers
from .serializers import BestsellerSerializer


# 베스트셀러 TOP20
@api_view(["GET"])
def bestseller_list(request):
    serializer = BestsellerSerializer(Bestsellers.objects.all(), many=True)
    return Response(serializer.data)


# 도서 검색
ALADIN_SEARCH_URL = "http://www.aladin.co.kr/ttb/api/ItemSearch.aspx"
TTB_KEY = "ttblsy74301608001"
VERSION = "20131101"

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
        "ttbkey": TTB_KEY,
        "Query": q,
        "QueryType": query_type,
        "SearchTarget": "Book",
        "Start": page,
        "MaxResults": min(size, 50),
        "Sort": sort,
        "CategoryId": category_id,
        "Output": "JS",
        "Version": VERSION,
    }

    res = requests.get(ALADIN_SEARCH_URL, params=params)
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