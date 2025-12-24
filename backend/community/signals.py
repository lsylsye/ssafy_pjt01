from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def seed_boards(sender, **kwargs):
    if sender.name != "community":
        return

    from .models import Board

    Board.objects.update_or_create(
        slug="free",
        defaults={"name": "자유게시판", "board_type": "FREE"},
    )
    Board.objects.update_or_create(
        slug="review",
        defaults={"name": "리뷰게시판", "board_type": "REVIEW"},
    )
