# mypage/urls.py
from django.urls import path
from .views import my_bookmarks

urlpatterns = [
    
    # 북마크 조회
    path("bookmarks/", my_bookmarks),

]
