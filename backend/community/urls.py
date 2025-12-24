from django.urls import path
from . import views

urlpatterns = [

    # FREE
    path("free/", views.free_list),
    path("free/write/", views.free_write),
    path("free/<int:post_id>/", views.free_detail),
    path("free/<int:post_id>/like/", views.post_like_toggle),
    path("free/<int:post_id>/comments/", views.free_comments_list),
    path("free/<int:post_id>/comments/write/", views.free_comments_write),
    path("free/<int:post_id>/comments/<int:comment_id>/", views.comment_delete),
    path("free/prefixes/", views.free_prefixes),


    # COMMENTS (global)
    path("comments/<int:comment_id>/", views.comment_delete),
    path("comments/<int:comment_id>/like/", views.comment_like_toggle),
]
