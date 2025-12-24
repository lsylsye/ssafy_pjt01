from django.urls import path
from . import views
from community.views import comment_delete

urlpatterns = [
    path("me/", views.my_review_list),
    path("write/", views.review_write),
    path("", views.review_list),
    path("<int:review_id>/", views.review_detail),
    path("<int:review_id>/like/", views.review_like_toggle),
    path("<int:review_id>/comments/", views.review_comments),
    path("<int:review_id>/comments/<int:comment_id>/", comment_delete),
    path("user/<int:user_id>/", views.user_review_list),
]
