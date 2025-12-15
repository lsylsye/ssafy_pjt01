from django.urls import path
from .views import bestseller_list
from .views import book_search

urlpatterns = [
    path("bestsellers/", bestseller_list),
    path("search/", book_search),
]
