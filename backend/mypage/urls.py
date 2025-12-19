# mypage/urls.py
from django.urls import path
from .views import my_profile, my_bookmarks

urlpatterns = [
    
    path("me/", my_profile),
    path("bookmarks/", my_bookmarks),

]
