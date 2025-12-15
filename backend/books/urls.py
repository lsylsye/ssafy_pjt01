from django.urls import path
from .views import bestseller_list

urlpatterns = [
    path("bestsellers/", bestseller_list),
]
