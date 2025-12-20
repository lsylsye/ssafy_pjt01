from django.urls import path
from .views import (
    community_boards,

    free_list, free_write, free_detail,
    review_list, review_write, review_detail,

    free_prefixes,

    free_comments_list, free_comments_write,
    review_comments_list, review_comments_write,

    comment_delete, comment_like_toggle,

    post_like_toggle, review_like_toggle,
)

urlpatterns = [
    # 커뮤니티별 게시판 목록
    path("<str:country>/", community_boards),

    # 자유 게시판
    path("<str:country>/free/", free_list),
    path("<str:country>/free/write", free_write),
    path("<str:country>/free/<int:post_id>/", free_detail),

    # 리뷰 게시판
    path("<str:country>/review/", review_list),
    path("<str:country>/review/write", review_write),
    path("<str:country>/review/<int:review_id>/", review_detail),

    # 말머리(자유만)
    path("<str:country>/free/prefixes/", free_prefixes),

    # 댓글(자유/리뷰)
    path("<str:country>/free/<int:post_id>/comments/", free_comments_list),
    path("<str:country>/free/<int:post_id>/comments/write", free_comments_write),

    path("<str:country>/review/<int:review_id>/comments/", review_comments_list),
    path("<str:country>/review/<int:review_id>/comments/write", review_comments_write),

    # 댓글 삭제/댓글 좋아요(전역)
    path("comments/<int:comment_id>/", comment_delete),
    path("comments/<int:comment_id>/like/", comment_like_toggle),

    # 글/리뷰 좋아요
    path("<str:country>/free/<int:post_id>/like/", post_like_toggle),
    path("<str:country>/review/<int:review_id>/like/", review_like_toggle),
]
