from django.urls import path
from . import views

urlpatterns = [
    # 커뮤니티별 게시판 목록
    path("<str:country>/", views.community_boards),

    # FREE
    path("<str:country>/free/", views.free_list),
    path("<str:country>/free/write/", views.free_write),
    path("<str:country>/free/<int:post_id>/", views.free_detail),
    path("<str:country>/free/<int:post_id>/like/", views.post_like_toggle),
    path("<str:country>/free/<int:post_id>/comments/", views.free_comments_list),
    path("<str:country>/free/<int:post_id>/comments/write/", views.free_comments_write),
    path("<str:country>/free/prefixes/", views.free_prefixes),

    # REVIEW
    path("<str:country>/review/", views.review_list),
    path("<str:country>/review/write/", views.review_write),
    path("<str:country>/review/<int:review_id>/", views.review_detail),
    path("<str:country>/review/<int:review_id>/like/", views.review_like_toggle),
    path("<str:country>/review/<int:review_id>/comments/", views.review_comments_list),
    path("<str:country>/review/<int:review_id>/comments/write/", views.review_comments_write),

    # COMMENTS (global)
    path("comments/<int:comment_id>/", views.comment_delete),
    path("comments/<int:comment_id>/like/", views.comment_like_toggle),
]
