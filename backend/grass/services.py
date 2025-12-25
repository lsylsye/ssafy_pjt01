from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .models import GrassDaily

POINTS = {
    "POST": 2,
    "REVIEW": 2,
    "COMMENT": 1,
}

# 레벨 구간별 필요 포인트 누적치 테이블 (Lv 1 ~ 20)
# Lv 1: 0
# Lv 2: 15, Lv 3: 30, Lv 4: 45
# Lv 5: 60, Lv 6: 90, Lv 7: 120, Lv 8: 150
# ...
def _get_level_threshold(lv):
    if lv <= 1: return 0
    # 스테이지(4개 레벨씩) 마다 경험치 요구량 증가
    # 1단계(씨앗): 15, 2단계(새싹): 30, 3단계(잔디): 50, 4단계(꽃): 80, 5단계(나무): 120, 6단계(숲): 160
    base_step = [15, 30, 50, 80, 120, 160]
    
    total = 0
    for i in range(1, min(lv, 25)):
        s_idx = (i - 1) // 4
        total += base_step[s_idx]
    return total


def level_from_exp(exp_total: int) -> int:
    if not exp_total or exp_total < 0:
        return 1
    
    for lv in range(24, 0, -1):
        if exp_total >= _get_level_threshold(lv):
            return lv
    return 1


def grass_bucket(points: int) -> str:
    if points <= 0:
        return "0"
    if points <= 1:
        return "1"
    if points <= 2:
        return "2"
    if points <= 3:
        return "3"
    return "3+"


@transaction.atomic
def add_points(user, action: str, when=None):
    if action not in POINTS:
        raise ValueError(f"Unknown action: {action}")

    if when is None:
        when = timezone.now()

    d = when.date() if hasattr(when, "date") else when
    pts = POINTS[action]

    # 1) 유저 누적 경험치 업데이트 (모든 활동 포함)
    if user.is_authenticated:
        user.exp_total = (user.exp_total or 0) + pts
        user.save(update_fields=["exp_total"])

    # 2) 일일 잔디 포인트 업데이트 (오직 리뷰만 반영, 1개당 1점)
    if action == "REVIEW":
        obj, _ = GrassDaily.objects.select_for_update().get_or_create(user=user, date=d)
        obj.points = (obj.points or 0) + 1
        obj.save(update_fields=["points", "updated_at"])
        return obj

    return None


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
        # 1개만 써도 이미 10000점이므로, 굳이 여기서 cap하지 않고 
        # 프론트엔드에서 넘어온 cap 값을 따르도록 count에 raw를 담아 보냄
        out.append({
            "date": cur.isoformat(),
            "count": raw,             # ✅ vue3-calendar-heatmap용
            "points": raw,
            "bucket": grass_bucket(raw),
        })
        cur += timedelta(days=1)

    return out


def get_level_payload(user):
    exp_total = getattr(user, "exp_total", 0) or 0
    level = level_from_exp(exp_total)
    
    current_start = _get_level_threshold(level)
    next_start = _get_level_threshold(level + 1) if level < 24 else current_start

    # 스테이지 및 명칭 규칙 적용
    stages = ["씨앗", "새싹", "잔디", "꽃", "나무", "숲"]
    suffixes = ["시작", "성장", "매일", "활발"]
    icons = ["seed", "sprout", "grass", "flower", "tree", "forest"]

    s_idx = (level - 1) // 4
    n_idx = (level - 1) % 4
    
    if s_idx >= len(stages): # 만렙 초과 방어
        s_idx = len(stages) - 1
        n_idx = 3

    title = f"{suffixes[n_idx]} {stages[s_idx]}"
    stage_num = s_idx + 1
    icon = icons[s_idx]

    denom = max(1, next_start - current_start)
    progress = (exp_total - current_start) / denom if level < 24 else 1.0
    progress = max(0.0, min(1.0, progress))

    return {
        "exp_total": exp_total,
        "level": level,
        "level_title": title,
        "level_stage": stage_num,
        "level_icon": icon,
        "current_level_start_exp": current_start,
        "next_level_start_exp": next_start,
        "level_progress": progress,   # 0~1
    }
