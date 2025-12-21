from django.urls import path
from .views import bestseller_list, new_special_list, book_search, book_detail, bookmark_toggle, my_bookmarks

urlpatterns = [

    # 도서 검색, 베스트셀러, 신간추천도서
    path("bestsellers/", bestseller_list),
    path("new/special/", new_special_list),
    path("search/", book_search),
    path("<str:isbn13>/", book_detail),
    # 북마크
    path("<str:isbn13>/bookmark/", bookmark_toggle),
    
]
