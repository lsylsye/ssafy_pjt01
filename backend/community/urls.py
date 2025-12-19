from django.urls import path
from .views import (
    community_boards,
    board_posts, post_detail,
    board_prefixes,
    board_reviews, review_detail,
    post_comments, review_comments,
)

urlpatterns = [
    # boards list
    path("<str:country>/", community_boards),

    # FREE posts
    path("<str:country>/<slug:board_slug>/posts/", board_posts),
    path("posts/<int:post_id>/", post_detail),
    path("posts/<int:post_id>/comments/", post_comments),

    # Prefixes (FREE only)
    path("<str:country>/<slug:board_slug>/prefixes/", board_prefixes),

    # Reviews
    path("<str:country>/<slug:board_slug>/reviews/", board_reviews),
    path("reviews/<int:review_id>/", review_detail),
    path("reviews/<int:review_id>/comments/", review_comments),
]
