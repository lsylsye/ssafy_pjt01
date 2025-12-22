from django.db import models
from django.conf import settings


class GrassDaily(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="grass_daily",
    )
    date = models.DateField()  # YYYY-MM-DD
    points = models.PositiveSmallIntegerField(default=0)  # 해당 날짜의 총점(원본)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "date"], name="unique_grass_daily_per_user_date"),
        ]
        indexes = [
            models.Index(fields=["user", "date"]),
        ]
        ordering = ["date"]

    def __str__(self):
        return f"{self.user_id}:{self.date}={self.points}"
