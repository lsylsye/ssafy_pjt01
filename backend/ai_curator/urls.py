# ai_curator/urls.py
from django.urls import path
from .views import recommend_book

urlpatterns = [
    path("recommend/", recommend_book, name="ai-curator-recommend"),
]
