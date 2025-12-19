from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def seed_communities_and_boards(sender, **kwargs):
    # community 앱 migrate 끝났을 때만 실행
    if sender.name != "community":
        return

    from .models import Community, Board

    defaults = [
        ("KR", "한국"),
        ("JP", "일본"),
        ("CN", "중화권"),
        ("EN", "영미권"),
    ]

    for country, name in defaults:
        community, _ = Community.objects.update_or_create(
            country=country,
            defaults={"name": name},
        )

        # 기본 게시판 2개 (free/review)
        Board.objects.update_or_create(
            community=community,
            slug="free",
            defaults={"name": "자유게시판", "board_type": "FREE"},
        )
        Board.objects.update_or_create(
            community=community,
            slug="review",
            defaults={"name": "리뷰게시판", "board_type": "REVIEW"},
        )
