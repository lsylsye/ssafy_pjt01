# mypage/urls.py
from django.urls import path
from .views import (
    my_profile, my_bookmarks, my_posts, my_comments,
    follow_toggle, followers_list, following_list, user_profile
)

urlpatterns = [
    path("me/", my_profile),
    path("bookmarks/", my_bookmarks),
    path("posts/", my_posts),
    path("comments/", my_comments),
    path("follow/<int:user_id>/", follow_toggle),
    path("followers/", followers_list),  # 내 팔로워
    path("followers/<int:user_id>/", followers_list),  # 특정 유저의 팔로워
    path("following/", following_list),  # 내 팔로잉
    path("following/<int:user_id>/", following_list),  # 특정 유저의 팔로잉
    path("profile/<int:user_id>/", user_profile),  # 다른 사용자 프로필 조회
]
