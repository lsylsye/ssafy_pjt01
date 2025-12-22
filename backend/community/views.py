from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from grass.services import add_points
from .models import Community, Board, Prefix, Post, Review, Comment, Like
from .serializers import (
    BoardSerializer,
    PrefixSerializer,
    PostListSerializer, PostWriteSerializer,
    ReviewListSerializer, ReviewWriteSerializer,
    CommentSerializer, CommentWriteSerializer,
)


def _auth_required(request):
    if not request.user.is_authenticated:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED
        )
    return None


def _normalize_country(country):
    return (country or "").lower().strip()


def _get_community(country):
    country = _normalize_country(country)
    return Community.objects.filter(country=country).first()


def _get_board(community, board_slug):
    return Board.objects.filter(community=community, slug=board_slug).first()


_CT_CACHE = {}


def _ct(model_cls):
    if model_cls not in _CT_CACHE:
        _CT_CACHE[model_cls] = ContentType.objects.get_for_model(model_cls)
    return _CT_CACHE[model_cls]


def _like_count_map(model_cls, obj_ids):
    if not obj_ids:
        return {}
    ct = _ct(model_cls)
    qs = (
        Like.objects
        .filter(content_type=ct, object_id__in=obj_ids)
        .values("object_id")
        .annotate(cnt=Count("id"))
    )
    return {row["object_id"]: row["cnt"] for row in qs}


def _comment_count_map(model_cls, obj_ids):
    if not obj_ids:
        return {}
    ct = _ct(model_cls)
    qs = (
        Comment.objects
        .filter(content_type=ct, object_id__in=obj_ids)
        .values("object_id")
        .annotate(cnt=Count("id"))
    )
    return {row["object_id"]: row["cnt"] for row in qs}


def _bulk_liked_ids(request, model_cls, obj_ids):
    if (not request.user.is_authenticated) or (not obj_ids):
        return set()
    ct = _ct(model_cls)
    return set(
        Like.objects
        .filter(user=request.user, content_type=ct, object_id__in=obj_ids)
        .values_list("object_id", flat=True)
    )


def _toggle_like(request, model_cls, obj_id):
    auth_resp = _auth_required(request)
    if auth_resp:
        return auth_resp

    ct = _ct(model_cls)
    like = Like.objects.filter(user=request.user, content_type=ct, object_id=obj_id).first()
    if like:
        like.delete()
        liked = False
    else:
        Like.objects.create(user=request.user, content_type=ct, object_id=obj_id)
        liked = True

    like_count = Like.objects.filter(content_type=ct, object_id=obj_id).count()
    return Response({"liked": liked, "like_count": like_count})


# 1) 커뮤니티별 게시판 목록: /api/community/<country>/
@api_view(["GET"])
def community_boards(request, country):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(BoardSerializer(community.boards.all(), many=True).data)


# 2) 자유 게시판 목록: /api/community/<country>/free/
@api_view(["GET"])
def free_list(request, country):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "free")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    qs = Post.objects.filter(board=board).select_related("user", "prefix").order_by("-id")

    # 검색(옵션): q=제목+내용, prefix=말머리
    q = (request.query_params.get("q") or "").strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))

    prefix = (request.query_params.get("prefix") or "").strip()
    if prefix:
        qs = qs.filter(prefix__name=prefix)

    post_ids = list(qs.values_list("id", flat=True))

    like_map = _like_count_map(Post, post_ids)
    comment_map = _comment_count_map(Post, post_ids)
    liked_ids = _bulk_liked_ids(request, Post, post_ids)

    data = []
    for p in qs:
        row = PostListSerializer(p, context={"liked_ids": liked_ids}).data
        row["like_count"] = like_map.get(p.id, 0)
        row["comment_count"] = comment_map.get(p.id, 0)
        data.append(row)

    return Response(data)


# 3) 자유 글 작성: /api/community/<country>/free/write/
@api_view(["POST"])
def free_write(request, country):
    auth_resp = _auth_required(request)
    if auth_resp:
        return auth_resp

    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "free")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    s = PostWriteSerializer(data=request.data)
    if not s.is_valid():
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    prefix_obj = None
    prefix_name = s.validated_data.get("prefix", "")
    if prefix_name:
        prefix_obj, _ = Prefix.objects.get_or_create(
            board=board,
            name=prefix_name,
            defaults={"created_by": request.user},
        )

    post = Post.objects.create(
        board=board,
        user=request.user,
        prefix=prefix_obj,
        title=s.validated_data["title"],
        content=s.validated_data["content"],
    )

    add_points(request.user, "POST") 

    row = PostListSerializer(post, context={"liked_ids": set()}).data
    row["like_count"] = 0
    row["comment_count"] = 0
    return Response(row, status=status.HTTP_201_CREATED)


# 4) 자유 글 상세/수정/삭제: /api/community/<country>/free/<post_id>/
@api_view(["GET", "PATCH", "DELETE"])
def free_detail(request, country, post_id):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "free")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    post = Post.objects.select_related("user", "prefix").filter(board=board, id=post_id).first()
    if post is None:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        like_map = _like_count_map(Post, [post.id])
        comment_map = _comment_count_map(Post, [post.id])
        liked_ids = _bulk_liked_ids(request, Post, [post.id])

        row = PostListSerializer(post, context={"liked_ids": liked_ids}).data
        row["like_count"] = like_map.get(post.id, 0)
        row["comment_count"] = comment_map.get(post.id, 0)
        return Response(row)

    auth_resp = _auth_required(request)
    if auth_resp:
        return auth_resp

    if post.user_id != request.user.id:
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PATCH
    if "title" in request.data:
        post.title = request.data.get("title")
    if "content" in request.data:
        post.content = request.data.get("content")
    if "prefix" in request.data:
        prefix_name = str(request.data.get("prefix") or "").strip()
        if prefix_name:
            prefix_obj, _ = Prefix.objects.get_or_create(
                board=board,
                name=prefix_name,
                defaults={"created_by": request.user},
            )
            post.prefix = prefix_obj
        else:
            post.prefix = None

    post.save()

    like_map = _like_count_map(Post, [post.id])
    comment_map = _comment_count_map(Post, [post.id])
    liked_ids = _bulk_liked_ids(request, Post, [post.id])

    row = PostListSerializer(post, context={"liked_ids": liked_ids}).data
    row["like_count"] = like_map.get(post.id, 0)
    row["comment_count"] = comment_map.get(post.id, 0)
    return Response(row)


# 5) 자유 글 좋아요 토글: /api/community/<country>/free/<post_id>/like/
@api_view(["POST"])
def post_like_toggle(request, country, post_id):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "free")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    if not Post.objects.filter(board=board, id=post_id).exists():
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    return _toggle_like(request, Post, post_id)


# 6) 자유 말머리 목록(옵션): /api/community/<country>/free/prefixes/
@api_view(["GET"])
def free_prefixes(request, country):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "free")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    qs = board.prefixes.all().order_by("name")
    return Response(PrefixSerializer(qs, many=True).data)


# -----------------------------
# 댓글 트리 공통
# -----------------------------
def _comment_tree_response(request, target_model, target_id):
    target_ct = _ct(target_model)
    comment_ct = _ct(Comment)

    qs = (
        Comment.objects
        .filter(content_type=target_ct, object_id=target_id)
        .select_related("user", "parent_comment")
        .order_by("id")
    )

    comment_ids = list(qs.values_list("id", flat=True))
    liked_comment_ids = _bulk_liked_ids(request, Comment, comment_ids)

    like_qs = (
        Like.objects
        .filter(content_type=comment_ct, object_id__in=comment_ids)
        .values("object_id")
        .annotate(cnt=Count("id"))
    )
    like_map = {row["object_id"]: row["cnt"] for row in like_qs}

    # 베스트(좋아요 10개 이상) Top3
    best_candidates = []
    for c in qs:
        lc = like_map.get(c.id, 0)
        if lc >= 10:
            best_candidates.append((lc, c.id, c))
    best_candidates.sort(key=lambda x: (-x[0], x[1]))
    best_top3 = best_candidates[:3]

    best = []
    for lc, _, c in best_top3:
        d = CommentSerializer(c, context={"liked_ids": liked_comment_ids}).data
        d["like_count"] = lc
        best.append(d)

    children = {}
    roots = []
    for c in qs:
        pid = c.parent_comment_id
        if pid:
            children.setdefault(pid, []).append(c)
        else:
            roots.append(c)

    def build_node(c):
        d = CommentSerializer(c, context={"liked_ids": liked_comment_ids}).data
        d["like_count"] = like_map.get(c.id, 0)
        d["replies"] = [build_node(ch) for ch in children.get(c.id, [])]
        return d

    return {"best": best, "comments": [build_node(c) for c in roots]}


# 7) 자유 댓글 목록: /api/community/<country>/free/<post_id>/comments/
@api_view(["GET"])
def free_comments_list(request, country, post_id):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "free")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    if not Post.objects.filter(board=board, id=post_id).exists():
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(_comment_tree_response(request, Post, post_id))


# 8) 자유 댓글 작성: /api/community/<country>/free/<post_id>/comments/write/
@api_view(["POST"])
def free_comments_write(request, country, post_id):
    auth_resp = _auth_required(request)
    if auth_resp:
        return auth_resp

    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "free")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    post = Post.objects.filter(board=board, id=post_id).first()
    if post is None:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    s = CommentWriteSerializer(data=request.data)
    if not s.is_valid():
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    parent_obj = None
    parent_id = s.validated_data.get("parent_comment_id")
    if parent_id:
        parent_obj = Comment.objects.filter(id=parent_id).first()
        if parent_obj is None:
            return Response({"error": "Parent comment not found"}, status=status.HTTP_404_NOT_FOUND)

        post_ct = _ct(Post)
        if parent_obj.content_type_id != post_ct.id or parent_obj.object_id != post.id:
            return Response({"error": "Parent comment target mismatch"}, status=status.HTTP_400_BAD_REQUEST)

    comment = Comment.objects.create(
        user=request.user,
        content_type=_ct(Post),
        object_id=post.id,
        parent_comment=parent_obj,
        content=s.validated_data["content"],
    )

    add_points(request.user, "COMMENT")

    row = CommentSerializer(comment, context={"liked_ids": set()}).data
    row["like_count"] = 0
    return Response(row, status=status.HTTP_201_CREATED)


# -----------------------------
# 리뷰 게시판
# -----------------------------

# 1) 리뷰 목록: /api/community/<country>/review/
@api_view(["GET"])
def review_list(request, country):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    qs = Review.objects.filter(board=board).select_related("user").order_by("-id")

    review_ids = list(qs.values_list("id", flat=True))
    like_map = _like_count_map(Review, review_ids)
    comment_map = _comment_count_map(Review, review_ids)
    liked_ids = _bulk_liked_ids(request, Review, review_ids)

    data = []
    for r in qs:
        row = ReviewListSerializer(r, context={"liked_ids": liked_ids}).data
        row["like_count"] = like_map.get(r.id, 0)
        row["comment_count"] = comment_map.get(r.id, 0)
        data.append(row)

    return Response(data)


# 2) 리뷰 작성: /api/community/<country>/review/write/
@api_view(["POST"])
def review_write(request, country):
    auth_resp = _auth_required(request)
    if auth_resp:
        return auth_resp

    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "review")
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

    row = ReviewListSerializer(review, context={"liked_ids": set()}).data
    row["like_count"] = 0
    row["comment_count"] = 0
    return Response(row, status=status.HTTP_201_CREATED)


# 3) 리뷰 상세/수정/삭제: /api/community/<country>/review/<review_id>/
@api_view(["GET", "PATCH", "DELETE"])
def review_detail(request, country, review_id):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    review = Review.objects.select_related("user").filter(board=board, id=review_id).first()
    if review is None:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        like_map = _like_count_map(Review, [review.id])
        comment_map = _comment_count_map(Review, [review.id])
        liked_ids = _bulk_liked_ids(request, Review, [review.id])

        row = ReviewListSerializer(review, context={"liked_ids": liked_ids}).data
        row["like_count"] = like_map.get(review.id, 0)
        row["comment_count"] = comment_map.get(review.id, 0)
        return Response(row)

    auth_resp = _auth_required(request)
    if auth_resp:
        return auth_resp

    if review.user_id != request.user.id:
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "DELETE":
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PATCH
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

    row = ReviewListSerializer(review, context={"liked_ids": liked_ids}).data
    row["like_count"] = like_map.get(review.id, 0)
    row["comment_count"] = comment_map.get(review.id, 0)
    return Response(row)


# 4) 리뷰 좋아요 토글: /api/community/<country>/review/<review_id>/like/
@api_view(["POST"])
def review_like_toggle(request, country, review_id):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    if not Review.objects.filter(board=board, id=review_id).exists():
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    return _toggle_like(request, Review, review_id)


# 5) 리뷰 댓글 목록: /api/community/<country>/review/<review_id>/comments/
@api_view(["GET"])
def review_comments_list(request, country, review_id):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    if not Review.objects.filter(board=board, id=review_id).exists():
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(_comment_tree_response(request, Review, review_id))


# 6) 리뷰 댓글 작성: /api/community/<country>/review/<review_id>/comments/write/
@api_view(["POST"])
def review_comments_write(request, country, review_id):
    auth_resp = _auth_required(request)
    if auth_resp:
        return auth_resp

    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    review = Review.objects.filter(board=board, id=review_id).first()
    if review is None:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

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

    row = CommentSerializer(comment, context={"liked_ids": set()}).data
    row["like_count"] = 0
    return Response(row, status=status.HTTP_201_CREATED)


# -----------------------------
# 댓글 전역
# -----------------------------

# 댓글 삭제: /api/community/comments/<comment_id>/
@api_view(["DELETE"])
def comment_delete(request, comment_id):
    auth_resp = _auth_required(request)
    if auth_resp:
        return auth_resp

    comment = Comment.objects.filter(id=comment_id).first()
    if comment is None:
        return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

    if comment.user_id != request.user.id:
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# 댓글 좋아요 토글: /api/community/comments/<comment_id>/like/
@api_view(["POST"])
def comment_like_toggle(request, comment_id):
    if not Comment.objects.filter(id=comment_id).exists():
        return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
    return _toggle_like(request, Comment, comment_id)
