from django.contrib.contenttypes.models import ContentType

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Community, Board, Prefix, Post, Review, Comment, Like
from .serializers import (
    BoardSerializer,
    PrefixSerializer,
    PostListSerializer, PostWriteSerializer,
    ReviewListSerializer, ReviewWriteSerializer,
    CommentSerializer, CommentWriteSerializer,
)

# 너의 books 로직 위치에 맞춰 import 경로만 맞춰줘
from books.services import get_or_create_book_by_isbn13


def _auth_required(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
    return None


def _get_community(country):
    return Community.objects.filter(country=country).first()


def _get_board(community, board_slug):
    return Board.objects.filter(community=community, slug=board_slug).first()


def _ct(model_cls):
    return ContentType.objects.get_for_model(model_cls)


def _like_count(model_cls, obj_id):
    ct = _ct(model_cls)
    return Like.objects.filter(content_type=ct, object_id=obj_id).count()


def _comment_count(model_cls, obj_id):
    ct = _ct(model_cls)
    return Comment.objects.filter(content_type=ct, object_id=obj_id).count()


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

    return Response({"liked": liked, "like_count": Like.objects.filter(content_type=ct, object_id=obj_id).count()})


# 1) 커뮤니티별 게시판 목록
@api_view(["GET"])
def community_boards(request, country):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(BoardSerializer(community.boards.all(), many=True).data)


# 2) 자유 게시판 글 목록
@api_view(["GET"])
def free_list(request, country):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "free")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    qs = Post.objects.filter(board=board).select_related("user", "prefix").order_by("-id")

    prefix = request.query_params.get("prefix")
    if prefix:
        qs = qs.filter(prefix__name=prefix)

    data = []
    for p in qs:
        row = PostListSerializer(p).data
        row["like_count"] = _like_count(Post, p.id)
        row["comment_count"] = _comment_count(Post, p.id)
        data.append(row)

    return Response(data)


# 2) 자유 글 작성: /free/write
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

    data = PostListSerializer(post).data
    data["like_count"] = 0
    data["comment_count"] = 0
    return Response(data, status=status.HTTP_201_CREATED)




# 3) 자유 글 상세/수정/삭제: /free/<post_id>/
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
        data = PostListSerializer(post).data
        data["like_count"] = _like_count(Post, post.id)
        data["comment_count"] = _comment_count(Post, post.id)
        return Response(data)

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

    data = PostListSerializer(post).data
    data["like_count"] = _like_count(Post, post.id)
    data["comment_count"] = _comment_count(Post, post.id)
    return Response(data)


# 2) 리뷰 목록
@api_view(["GET"])
def review_list(request, country):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    qs = Review.objects.filter(board=board).select_related("user", "book").order_by("-id")

    data = []
    for r in qs:
        row = ReviewListSerializer(r).data
        row["like_count"] = _like_count(Review, r.id)
        row["comment_count"] = _comment_count(Review, r.id)
        data.append(row)

    return Response(data)


# 2) 리뷰 작성: /review/write
@api_view(["POST"])
def review_write(request, country):
    # 로그인 필요
    auth_resp = _auth_required(request)
    if auth_resp:
        return auth_resp

    # 커뮤니티/보드 확인
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    # 입력 검증
    s = ReviewWriteSerializer(data=request.data)
    if not s.is_valid():
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    v = s.validated_data

    # Review 생성
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

    data = ReviewListSerializer(review).data
    data["like_count"] = 0
    data["comment_count"] = 0
    return Response(data, status=status.HTTP_201_CREATED)


# 3) 리뷰 상세/수정/삭제: /review/<review_id>/
@api_view(["GET", "PATCH", "DELETE"])
def review_detail(request, country, review_id):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, "review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    review = Review.objects.select_related("user", "book").filter(board=board, id=review_id).first()
    if review is None:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        data = ReviewListSerializer(review).data
        data["like_count"] = _like_count(Review, review.id)
        data["comment_count"] = _comment_count(Review, review.id)
        return Response(data)

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
        try:
            rating = int(request.data.get("rating"))
        except Exception:
            return Response({"error": "rating must be int"}, status=status.HTTP_400_BAD_REQUEST)
        if rating < 1 or rating > 5:
            return Response({"error": "rating must be 1~5"}, status=status.HTTP_400_BAD_REQUEST)
        review.rating = rating

    if "content" in request.data:
        review.content = request.data.get("content")

    review.save()

    data = ReviewListSerializer(review).data
    data["like_count"] = _like_count(Review, review.id)
    data["comment_count"] = _comment_count(Review, review.id)
    return Response(data)


# 4) 말머리(자유만): /free/prefixes/
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



def _comment_tree_response(target_model, target_id):
    target_ct = _ct(target_model)
    comment_ct = _ct(Comment)

    qs = Comment.objects.filter(content_type=target_ct, object_id=target_id).select_related("user", "parent_comment").order_by("id")

    # like_count map
    like_map = {}
    for c in qs:
        like_map[c.id] = Like.objects.filter(content_type=comment_ct, object_id=c.id).count()

    # 베스트(좋아요 10개 이상) Top3: likes desc, id asc
    best_candidates = []
    for c in qs:
        lc = like_map.get(c.id, 0)
        if lc >= 10:
            best_candidates.append((lc, c.id, c))
    best_candidates.sort(key=lambda x: (-x[0], x[1]))
    best_top3 = best_candidates[:3]

    best = []
    for lc, _, c in best_top3:
        d = CommentSerializer(c).data
        d["like_count"] = lc
        best.append(d)

    # 트리 구성
    children = {}
    roots = []

    for c in qs:
        pid = c.parent_comment_id
        if pid:
            children.setdefault(pid, []).append(c)
        else:
            roots.append(c)

    def build_node(c):
        d = CommentSerializer(c).data
        d["like_count"] = like_map.get(c.id, 0)
        d["replies"] = [build_node(ch) for ch in children.get(c.id, [])]
        return d

    return {"best": best, "comments": [build_node(c) for c in roots]}


# 5) 댓글 목록(자유): /free/<post_id>/comments/
@api_view(["GET"])
def free_comments_list(request, country, post_id):
    # 존재 확인
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)
    board = _get_board(community, "free")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    exists = Post.objects.filter(board=board, id=post_id).exists()
    if not exists:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(_comment_tree_response(Post, post_id))


# 5) 댓글 작성(자유): /free/<post_id>/comments/write
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
    if "parent_comment_id" in s.validated_data:
        parent_id = s.validated_data["parent_comment_id"]
        parent_obj = Comment.objects.filter(id=parent_id).first()
        if parent_obj is None:
            return Response({"error": "Parent comment not found"}, status=status.HTTP_404_NOT_FOUND)

        # 부모 댓글이 같은 대상(Post)에 달린 댓글인지 검증
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

    data = CommentSerializer(comment).data
    data["like_count"] = 0
    return Response(data, status=status.HTTP_201_CREATED)


# 5) 댓글 목록(리뷰): /review/<review_id>/comments/
@api_view(["GET"])
def review_comments_list(request, country, review_id):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)
    board = _get_board(community, "review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    exists = Review.objects.filter(board=board, id=review_id).exists()
    if not exists:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(_comment_tree_response(Review, review_id))


# 5) 댓글 작성(리뷰): /review/<review_id>/comments/write
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
    if "parent_comment_id" in s.validated_data:
        parent_id = s.validated_data["parent_comment_id"]
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

    data = CommentSerializer(comment).data
    data["like_count"] = 0
    return Response(data, status=status.HTTP_201_CREATED)


# 댓글 삭제(전역): /comments/<comment_id>/
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


# 댓글 좋아요 토글(전역): /comments/<comment_id>/like/
@api_view(["POST"])
def comment_like_toggle(request, comment_id):
    exists = Comment.objects.filter(id=comment_id).exists()
    if not exists:
        return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
    return _toggle_like(request, Comment, comment_id)


# 글 좋아요 토글: /free/<post_id>/like/
@api_view(["POST"])
def post_like_toggle(request, country, post_id):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)
    board = _get_board(community, "free")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    exists = Post.objects.filter(board=board, id=post_id).exists()
    if not exists:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    return _toggle_like(request, Post, post_id)


# 리뷰 좋아요 토글: /review/<review_id>/like/
@api_view(["POST"])
def review_like_toggle(request, country, review_id):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)
    board = _get_board(community, "review")
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    exists = Review.objects.filter(board=board, id=review_id).exists()
    if not exists:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    return _toggle_like(request, Review, review_id)
