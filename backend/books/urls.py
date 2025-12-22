from django.urls import path
from .views import (
    bestseller_list,
    new_special_list,
    book_search,
    book_detail,
    bookmark_toggle,
    RecommendBookmarkBasedView,
    RecommendFollowBasedView,
    RecommendDebugView,
)

urlpatterns = [
    # 도서 검색, 베스트셀러, 신간추천도서
    path("bestsellers/", bestseller_list),
    path("new/special/", new_special_list),
    path("search/", book_search),

    
    # 추천알고리즘
    path("recommend/bookmark/", RecommendBookmarkBasedView.as_view()),
    path("recommend/follow/", RecommendFollowBasedView.as_view()),
    path("recommend/debug/", RecommendDebugView.as_view()),

    # 북마크
    path("<str:isbn13>/bookmark/", bookmark_toggle),

    # 도서상세
    path("<str:isbn13>/", book_detail),
]
