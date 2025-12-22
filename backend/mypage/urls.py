# mypage/urls.py
from django.urls import path
from .views import my_profile, my_bookmarks, my_posts, my_comments

urlpatterns = [
    path("me/", my_profile),
    path("bookmarks/", my_bookmarks),
    path("posts/", my_posts),
    path("comments/", my_comments),

]
