from django.urls import path
from .views import bestseller_list, book_search, book_detail

urlpatterns = [
    path("bestsellers/", bestseller_list),
    path("search/", book_search),
    path("<str:isbn13>/", book_detail),
]
