from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .models import GrassDaily

POINTS = {
    "POST": 2,
    "REVIEW": 2,
    "COMMENT": 1,
}


def level_from_exp(exp_total: int) -> int:
    if exp_total is None:
        exp_total = 0
    if exp_total < 0:
        exp_total = 0

    level = 1
    while True:
        next_level = level + 1
        next_start = 10 * (next_level - 1) * next_level // 2
        if exp_total >= next_start:
            level = next_level
        else:
            break
    return level


def grass_bucket(points: int) -> str:
    if points <= 0:
        return "0"
    if points <= 2:
        return "1-2"
    if points <= 5:
        return "3-5"
    if points <= 9:
        return "6-9"
    return "10+"


@transaction.atomic
def add_points(user, action: str, when=None):
    if action not in POINTS:
        raise ValueError(f"Unknown action: {action}")

    if when is None:
        when = timezone.now()

    d = when.date() if hasattr(when, "date") else when
    pts = POINTS[action]

    obj, _ = GrassDaily.objects.select_for_update().get_or_create(user=user, date=d)
    obj.points = (obj.points or 0) + pts
    obj.save(update_fields=["points", "updated_at"])

    if hasattr(user, "exp_total"):
        user.exp_total = (user.exp_total or 0) + pts
        user.save(update_fields=["exp_total"])

    return obj


def get_grass_range(user, days=365, end_date=None):
    if end_date is None:
        end_date = timezone.localdate()

    days = max(1, min(int(days), 365))
    start = end_date - timedelta(days=days - 1)

    qs = (
        GrassDaily.objects
        .filter(user=user, date__gte=start, date__lte=end_date)
        .values("date", "points")
    )
    m = {row["date"]: row["points"] for row in qs}

    out = []
    cur = start
    while cur <= end_date:
        raw = int(m.get(cur, 0) or 0)
        capped = min(raw, 10)
        out.append({
            "date": cur.isoformat(),
            "count": capped,          # ✅ vue3-calendar-heatmap용
            "points": raw,            # (옵션) 원본
            "bucket": grass_bucket(capped),
        })
        cur += timedelta(days=1)

    return out


def get_level_payload(user):
    exp_total = getattr(user, "exp_total", 0) or 0
    level = level_from_exp(exp_total)

    current_start = 10 * (level - 1) * level // 2
    next_start = 10 * level * (level + 1) // 2

    denom = max(1, next_start - current_start)
    progress = (exp_total - current_start) / denom
    if progress < 0:
        progress = 0.0
    if progress > 1:
        progress = 1.0

    return {
        "exp_total": exp_total,
        "level": level,
        "current_level_start_exp": current_start,
        "next_level_start_exp": next_start,
        "level_progress": progress,   # 0~1
    }
