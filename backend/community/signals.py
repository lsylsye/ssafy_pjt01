from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def seed_community(sender, **kwargs):
    if sender.name != "community":
        return

    from .models import Community, Board

    defaults = [
        ("kr", "한국"),
        ("jp", "일본"),
        ("cn", "중화권"),
        ("en", "영미권"),
    ]

    for country, name in defaults:
        community, _ = Community.objects.update_or_create(
            country=country,
            defaults={"name": name},
        )

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
