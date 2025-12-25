# ai_curator/urls.py
from django.urls import path
from .views import recommend_book, book_ai_review, book_travel, get_supported_countries

urlpatterns = [
    path("recommend/", recommend_book, name="ai-curator-recommend"),
    path("travel/", book_travel, name="book-travel"),
    path("travel/countries/", get_supported_countries, name="supported-countries"),
    path("<str:isbn13>/", book_ai_review, name="book-ai-review"),
]

