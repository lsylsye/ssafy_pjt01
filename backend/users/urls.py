from django.urls import path
from .views import follow_toggle, followers_list, following_list

urlpatterns = [
    path("<int:user_id>/follow/", follow_toggle),
    path("<int:user_id>/followers/", followers_list),
    path("<int:user_id>/following/", following_list),
]
