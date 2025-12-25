from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import get_grass_range, get_level_payload

User = get_user_model()


class GrassMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # vue3-calendar-heatmap: endDate 주면 1년 자동 생성됨
        # 우리는 values만 주면 되지만, 프론트 편하게 end_date도 같이 내려줌
        days = int(request.query_params.get("days", 365))
        days = max(1, min(days, 365))

        items = get_grass_range(request.user, days=days)

        return Response({
            "user_id": request.user.id,
            "days": days,
            "end_date": date.today().isoformat(),
            "values": [{"date": x["date"], "count": x["count"]} for x in items],
            "legend": ["0", "1", "2", "3", "3+"],
            "cap": 3,
        })


class GrassUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        target = get_object_or_404(User, id=user_id)

        days = int(request.query_params.get("days", 365))
        days = max(1, min(days, 365))

        items = get_grass_range(target, days=days)

        return Response({
            "user_id": target.id,
            "days": days,
            "end_date": items[-1]["date"] if items else None,
            "values": [{"date": x["date"], "count": x["count"]} for x in items],
            "legend": ["0", "1", "2", "3", "3+"],
            "cap": 3,
        })


class LevelMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(get_level_payload(request.user))


class LevelUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        return Response(get_level_payload(target))


class GrassSyncView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from reviews.models import Review
        from .models import GrassDaily
        from django.db.models import Count
        from django.db.models.functions import TruncDate
        
        user = request.user
        
        # 1. 해당 유저의 모든 잔디 기록을 0으로 초기화 (잘못된 과거 데이터 제거)
        GrassDaily.objects.filter(user=user).update(points=0)
        
        # 2. 리뷰 DB를 전수 조사하여 날짜별 개수 파악
        review_counts = (
            Review.objects.filter(user=user)
            .annotate(date_only=TruncDate('created_at'))
            .values('date_only')
            .annotate(count=Count('id'))
        )
        
        # 3. 파악된 개수를 잔디 DB에 덮어쓰기
        for entry in review_counts:
            d = entry['date_only']
            cnt = entry['count']
            obj, _ = GrassDaily.objects.get_or_create(user=user, date=d)
            obj.points = cnt
            obj.save()
        
        return Response({
            "message": "과거 기록을 포함한 모든 잔디 데이터가 리뷰 기준으로 재구성되었습니다.",
            "synced_days": len(review_counts)
        })
