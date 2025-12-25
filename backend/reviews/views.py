from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from grass.services import add_points
from community.models import Board, Comment, Like
from community.views import (
    _auth_required, _get_board_by_slug, _ct, 
    _like_count_map, _comment_count_map, _bulk_liked_ids, _toggle_like,
    _comment_tree_response
)
from .models import Review
from .serializers import ReviewListSerializer, ReviewWriteSerializer

# 1) 리뷰 목록
@api_view(["GET"])
def review_list(request):
    board = _get_board_by_slug("review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    qs = Review.objects.filter(board=board).select_related("user").order_by("-created_at", "-id")

    review_ids = list(qs.values_list("id", flat=True))
    like_map = _like_count_map(Review, review_ids)
    comment_map = _comment_count_map(Review, review_ids)
    liked_ids = _bulk_liked_ids(request, Review, review_ids)

    data = []
    for r in qs:
        row = ReviewListSerializer(r, context={"request": request, "liked_ids": liked_ids}).data
        row["like_count"] = like_map.get(r.id, 0)
        row["comment_count"] = comment_map.get(r.id, 0)
        data.append(row)

    return Response(data)

# 2) 리뷰 작성
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def review_write(request):
    board = _get_board_by_slug("review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    s = ReviewWriteSerializer(data=request.data)
    if not s.is_valid():
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    v = s.validated_data

    review = Review.objects.create(
        board=board,
        user=request.user,
        book_title=v["book_title"],
        book_author=v["book_author"],
        content=v["content"],
        rating=v.get("rating", None),
        isbn13=v.get("isbn13", ""),
        publisher=v.get("publisher", ""),
        pub_date=v.get("pub_date", ""),
        cover=v.get("cover", ""),
    )

    add_points(request.user, "REVIEW")

    row = ReviewListSerializer(review, context={"request": request, "liked_ids": set()}).data
    row["like_count"] = 0
    row["comment_count"] = 0
    
    # 레벨 업 정보 추가
    from grass.services import get_level_payload
    row["level_info"] = get_level_payload(request.user)

    return Response(row, status=status.HTTP_201_CREATED)

# 3) 리뷰 상세/수정/삭제
@api_view(["GET", "PATCH", "DELETE"])
def review_detail(request, review_id):
    board = _get_board_by_slug("review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    review = Review.objects.select_related("user").filter(board=board, id=review_id).first()
    if review is None:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        like_map = _like_count_map(Review, [review.id])
        comment_map = _comment_count_map(Review, [review.id])
        liked_ids = _bulk_liked_ids(request, Review, [review.id])

        row = ReviewListSerializer(review, context={"request": request, "liked_ids": liked_ids}).data
        row["like_count"] = like_map.get(review.id, 0)
        row["comment_count"] = comment_map.get(review.id, 0)
        return Response(row)

    # 401을 피하기 위해 DRF standard 활용 권장하지만 
    # 일단 PATCH/DELETE에도 인증이 필요하므로 수동체크 유지 혹은 위 래퍼 수정
    auth_resp = _auth_required(request)
    if auth_resp:
        return auth_resp

    if review.user_id != request.user.id:
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "DELETE":
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if "rating" in request.data:
        rating = request.data.get("rating")
        if rating is not None and rating != "":
            try:
                rating = int(rating)
            except Exception:
                return Response({"error": "rating must be int"}, status=status.HTTP_400_BAD_REQUEST)
            if rating < 1 or rating > 5:
                return Response({"error": "rating must be 1~5"}, status=status.HTTP_400_BAD_REQUEST)
            review.rating = rating
        else:
            review.rating = None

    if "content" in request.data:
        review.content = request.data.get("content")

    review.save()

    like_map = _like_count_map(Review, [review.id])
    comment_map = _comment_count_map(Review, [review.id])
    liked_ids = _bulk_liked_ids(request, Review, [review.id])

    row = ReviewListSerializer(review, context={"request": request, "liked_ids": liked_ids}).data
    row["like_count"] = like_map.get(review.id, 0)
    row["comment_count"] = comment_map.get(review.id, 0)
    return Response(row)

# 4) 리뷰 좋아요 토글
@api_view(["POST"])
def review_like_toggle(request, review_id):
    board = _get_board_by_slug("review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    if not Review.objects.filter(board=board, id=review_id).exists():
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    return _toggle_like(request, Review, review_id)

# 5) 리뷰 댓글 목록/작성
@api_view(["GET", "POST"])
def review_comments(request, review_id):
    board = _get_board_by_slug("review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    review = Review.objects.filter(board=board, id=review_id).first()
    if review is None:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        auth_resp = _auth_required(request)
        if auth_resp:
            return auth_resp

        from community.serializers import CommentWriteSerializer, CommentSerializer
        s = CommentWriteSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

        parent_obj = None
        parent_id = s.validated_data.get("parent_comment_id")
        if parent_id:
            parent_obj = Comment.objects.filter(id=parent_id).first()
            if parent_obj is None:
                return Response({"error": "Parent comment not found"}, status=status.HTTP_404_NOT_FOUND)

            review_ct = _ct(Review)
            if parent_obj.content_type_id != review_ct.id or parent_obj.object_id != review.id:
                return Response({"error": "Parent comment target mismatch"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(
            user=request.user,
            content_type=_ct(Review),
            object_id=review.id,
            parent_comment=parent_obj,
            content=s.validated_data["content"],
        )

        add_points(request.user, "COMMENT")

        row = CommentSerializer(comment, context={"request": request, "liked_ids": set()}).data
        row["like_count"] = 0
        
        # 레벨 업 정보 추가
        from grass.services import get_level_payload
        row["level_info"] = get_level_payload(request.user)

        return Response(row, status=status.HTTP_201_CREATED)

    return Response(_comment_tree_response(request, Review, review_id))

# 6) 사용자별 리뷰 목록
@api_view(["GET"])
def user_review_list(request, user_id):
    board = _get_board_by_slug("review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    qs = Review.objects.filter(board=board, user_id=user_id).select_related("user").order_by("-created_at", "-id")

    review_ids = list(qs.values_list("id", flat=True))
    like_map = _like_count_map(Review, review_ids)
    comment_map = _comment_count_map(Review, review_ids)
    liked_ids = _bulk_liked_ids(request, Review, review_ids)

    data = []
    for r in qs:
        row = ReviewListSerializer(r, context={"request": request, "liked_ids": liked_ids}).data
        row["like_count"] = like_map.get(r.id, 0)
        row["comment_count"] = comment_map.get(r.id, 0)
        data.append(row)

    return Response(data)


# 7) 내가 쓴 리뷰 목록
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_review_list(request):
    board = _get_board_by_slug("review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    qs = Review.objects.filter(board=board, user=request.user).select_related("user").order_by("-created_at", "-id")

    review_ids = list(qs.values_list("id", flat=True))
    like_map = _like_count_map(Review, review_ids)
    comment_map = _comment_count_map(Review, review_ids)
    liked_ids = _bulk_liked_ids(request, Review, review_ids)

    data = []
    for r in qs:
        row = ReviewListSerializer(r, context={"request": request, "liked_ids": liked_ids}).data
        row["like_count"] = like_map.get(r.id, 0)
        row["comment_count"] = comment_map.get(r.id, 0)
        data.append(row)

    return Response(data)


# 8) 오늘 내가 쓴 리뷰 목록
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def today_reviews(request):
    from django.utils import timezone
    today = timezone.localdate()
    
    qs = Review.objects.filter(
        user=request.user, 
        created_at__date=today
    ).order_by("-created_at", "-id")
    
    data = ReviewListSerializer(qs, many=True, context={"request": request, "liked_ids": set()}).data
    return Response(data)
