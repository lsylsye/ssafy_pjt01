from django.urls import path
from .views import follow_toggle, followers_list, following_list, profile_detail

urlpatterns = [
    path("<int:user_id>/follow/", follow_toggle),
    path("<int:user_id>/followers/", followers_list),
    path("<int:user_id>/following/", following_list),
    path("profile/<int:user_id>/", profile_detail),
]
