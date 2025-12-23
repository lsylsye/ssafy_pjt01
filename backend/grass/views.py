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
            "legend": ["0", "1-2", "3-5", "6-9", "10+"],
            "cap": 10,
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
            "legend": ["0", "1-2", "3-5", "6-9", "10+"],
            "cap": 10,
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
