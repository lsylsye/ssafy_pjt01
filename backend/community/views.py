# backend/community/views.py

from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from grass.services import add_points
from .models import Board, Prefix, Post, Comment, Like
from .serializers import (
    BoardSerializer,
    PrefixSerializer,
    PostListSerializer, PostWriteSerializer,
    CommentSerializer, CommentWriteSerializer,
)


def _auth_required(request):
    if not request.user.is_authenticated:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED
        )
    return None


def _get_board_by_slug(board_slug):
    return Board.objects.filter(slug=board_slug).first()


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


# (옵션) 게시판 목록: /api/community/boards/
@api_view(["GET"])
def boards_list(request):
    qs = Board.objects.all().order_by("slug")
    return Response(BoardSerializer(qs, many=True).data)


# -----------------------------
# FREE
# -----------------------------

# 1) 자유 게시판 목록: /api/community/free/
@api_view(["GET"])
def free_list(request):
    board = _get_board_by_slug("free")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    qs = Post.objects.filter(board=board).select_related("user", "prefix").order_by("-id")

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
        row = PostListSerializer(p, context={"request": request, "liked_ids": liked_ids}).data
        row["like_count"] = like_map.get(p.id, 0)
        row["comment_count"] = comment_map.get(p.id, 0)
        data.append(row)

    return Response(data)


# 2) 자유 글 작성: /api/community/free/write/
@api_view(["POST"])
def free_write(request):
    auth_resp = _auth_required(request)
    if auth_resp:
        return auth_resp

    board = _get_board_by_slug("free")
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

    row = PostListSerializer(post, context={"request": request, "liked_ids": set()}).data
    row["like_count"] = 0
    row["comment_count"] = 0

    # 레벨 업 정보 추가
    from grass.services import get_level_payload
    row["level_info"] = get_level_payload(request.user)

    return Response(row, status=status.HTTP_201_CREATED)


# 3) 자유 글 상세/수정/삭제: /api/community/free/<post_id>/
@api_view(["GET", "PATCH", "DELETE"])
def free_detail(request, post_id):
    board = _get_board_by_slug("free")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    post = Post.objects.select_related("user", "prefix").filter(board=board, id=post_id).first()
    if post is None:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        like_map = _like_count_map(Post, [post.id])
        comment_map = _comment_count_map(Post, [post.id])
        liked_ids = _bulk_liked_ids(request, Post, [post.id])

        row = PostListSerializer(post, context={"request": request, "liked_ids": liked_ids}).data
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

    row = PostListSerializer(post, context={"request": request, "liked_ids": liked_ids}).data
    row["like_count"] = like_map.get(post.id, 0)
    row["comment_count"] = comment_map.get(post.id, 0)
    return Response(row)


# 4) 자유 글 좋아요 토글: /api/community/free/<post_id>/like/
@api_view(["POST"])
def post_like_toggle(request, post_id):
    board = _get_board_by_slug("free")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    if not Post.objects.filter(board=board, id=post_id).exists():
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    return _toggle_like(request, Post, post_id)


# 5) 자유 말머리 목록: /api/community/free/prefixes/
@api_view(["GET"])
def free_prefixes(request):
    board = _get_board_by_slug("free")
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

    best_candidates = []
    for c in qs:
        lc = like_map.get(c.id, 0)
        if lc >= 10:
            best_candidates.append((lc, c.id, c))
    best_candidates.sort(key=lambda x: (-x[0], x[1]))
    best_top3 = best_candidates[:3]

    best = []
    for lc, _, c in best_top3:
        d = CommentSerializer(c, context={"request": request, "liked_ids": liked_comment_ids}).data
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
        d = CommentSerializer(c, context={"request": request, "liked_ids": liked_comment_ids}).data
        d["like_count"] = like_map.get(c.id, 0)
        d["replies"] = [build_node(ch) for ch in children.get(c.id, [])]
        return d

    return {"best": best, "comments": [build_node(c) for c in roots]}


# 6) 자유 댓글 목록: /api/community/free/<post_id>/comments/
@api_view(["GET"])
def free_comments_list(request, post_id):
    board = _get_board_by_slug("free")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    if not Post.objects.filter(board=board, id=post_id).exists():
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(_comment_tree_response(request, Post, post_id))


# 7) 자유 댓글 작성: /api/community/free/<post_id>/comments/write/
@api_view(["POST"])
def free_comments_write(request, post_id):
    auth_resp = _auth_required(request)
    if auth_resp:
        return auth_resp

    board = _get_board_by_slug("free")
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

    row = CommentSerializer(comment, context={"request": request, "liked_ids": set()}).data
    row["like_count"] = 0

    # 레벨 업 정보 추가
    from grass.services import get_level_payload
    row["level_info"] = get_level_payload(request.user)

    return Response(row, status=status.HTTP_201_CREATED)


# -----------------------------
# 댓글 전역
# -----------------------------

@api_view(["DELETE"])
def comment_delete(request, comment_id, **kwargs):
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


@api_view(["POST"])
def comment_like_toggle(request, comment_id):
    if not Comment.objects.filter(id=comment_id).exists():
        return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
    return _toggle_like(request, Comment, comment_id)
