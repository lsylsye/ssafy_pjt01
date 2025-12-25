from django.urls import path
from . import views
from .views import GrassMeView, GrassUserView, LevelMeView, LevelUserView

urlpatterns = [
    # 잔디
    path("me/", GrassMeView.as_view()),
    path("sync-today/", views.GrassSyncView.as_view()),
    path("users/<int:user_id>/", GrassUserView.as_view()),

    # 레벨/경험치
    path("level/me/", LevelMeView.as_view()),
    path("level/users/<int:user_id>/", LevelUserView.as_view()),
]
