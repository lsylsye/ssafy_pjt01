from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import Follow
from .serializers import SimpleUserSerializer

User = get_user_model()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_toggle(request, user_id):
    me = request.user
    target = get_object_or_404(User, id=user_id)

    if me.id == target.id:
        return Response({"error": "cannot follow yourself"}, status=400)

    rel = Follow.objects.filter(from_user=me, to_user=target).first()
    if rel:
        rel.delete()
        return Response({"followed": False})
    Follow.objects.create(from_user=me, to_user=target)
    return Response({"followed": True})


@api_view(["GET"])
def followers_list(request, user_id):
    target = get_object_or_404(User, id=user_id)

    qs = (
        Follow.objects
        .filter(to_user=target)
        .select_related("from_user")
        .order_by("-created_at")
    )
    users = [rel.from_user for rel in qs]
    return Response(SimpleUserSerializer(users, many=True).data)


@api_view(["GET"])
def following_list(request, user_id):
    target = get_object_or_404(User, id=user_id)

    qs = (
        Follow.objects
        .filter(from_user=target)
        .select_related("to_user")
        .order_by("-created_at")
    )
    users = [rel.to_user for rel in qs]
    return Response(SimpleUserSerializer(users, many=True).data)