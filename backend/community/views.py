from django.contrib.contenttypes.models import ContentType

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Community, Board, Prefix, Post, Review, Comment
from .serializers import (
    BoardSerializer,
    PrefixSerializer,
    PostSerializer, PostCreateSerializer,
    ReviewSerializer, ReviewCreateSerializer,
    CommentSerializer,
)

from books.services import get_or_create_book_by_isbn13  # 네가 만든 함수 경로에 맞춰 사용


def _get_community(country):
    return Community.objects.filter(country=country).first()


def _get_board(community, board_slug):
    return Board.objects.filter(community=community, slug=board_slug).first()


@api_view(["GET"])
def community_boards(request, country):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    boards = community.boards.all()
    return Response(BoardSerializer(boards, many=True).data, status=status.HTTP_200_OK)


# ---------- FREE POSTS ----------
@api_view(["GET", "POST"])
def board_posts(request, country, board_slug):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, board_slug)
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    if board.board_type != "FREE":
        return Response({"error": "This board is not FREE board"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        qs = Post.objects.filter(board=board).select_related("user", "prefix").order_by("-id")

        prefix = request.query_params.get("prefix")
        if prefix:
            qs = qs.filter(prefix__name=prefix)

        return Response(PostSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    # POST
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = PostCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    prefix_obj = None
    prefix_name = serializer.validated_data.get("prefix", "").strip()
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
        title=serializer.validated_data["title"],
        content=serializer.validated_data["content"],
    )
    return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)


@api_view(["PATCH", "DELETE", "GET"])
def post_detail(request, post_id):
    post = Post.objects.select_related("user", "prefix", "board", "board__community").filter(id=post_id).first()
    if post is None:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(PostSerializer(post).data, status=status.HTTP_200_OK)

    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    if post.user_id != request.user.id:
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PATCH
    serializer = PostCreateSerializer(data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if "title" in serializer.validated_data:
        post.title = serializer.validated_data["title"]
    if "content" in serializer.validated_data:
        post.content = serializer.validated_data["content"]

    if "prefix" in serializer.validated_data:
        prefix_name = serializer.validated_data.get("prefix", "").strip()
        if prefix_name:
            prefix_obj, _ = Prefix.objects.get_or_create(
                board=post.board,
                name=prefix_name,
                defaults={"created_by": request.user},
            )
            post.prefix = prefix_obj
        else:
            post.prefix = None

    post.save()
    return Response(PostSerializer(post).data, status=status.HTTP_200_OK)


# ---------- PREFIXES (FREE only) ----------
@api_view(["GET", "POST"])
def board_prefixes(request, country, board_slug):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, board_slug)
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    if board.board_type != "FREE":
        return Response({"error": "Prefixes only allowed on FREE board"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        qs = Prefix.objects.filter(board=board).order_by("name")
        return Response(PrefixSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    # POST
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = PrefixSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    prefix, _ = Prefix.objects.get_or_create(
        board=board,
        name=serializer.validated_data["name"],
        defaults={"created_by": request.user},
    )
    return Response(PrefixSerializer(prefix).data, status=status.HTTP_201_CREATED)


# ---------- REVIEWS ----------
@api_view(["GET", "POST"])
def board_reviews(request, country, board_slug):
    community = _get_community(country)
    if community is None:
        return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

    board = _get_board(community, board_slug)
    if board is None:
        return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    if board.board_type != "REVIEW":
        return Response({"error": "This board is not REVIEW board"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        qs = Review.objects.filter(board=board).select_related("user", "book").order_by("-id")
        return Response(ReviewSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    # POST
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = ReviewCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    isbn13 = serializer.validated_data["isbn13"]
    book = get_or_create_book_by_isbn13(isbn13)

    review = Review.objects.create(
        board=board,
        user=request.user,
        book=book,
        rating=serializer.validated_data["rating"],
        content=serializer.validated_data["content"],
    )
    return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
def review_detail(request, review_id):
    review = Review.objects.select_related("user", "book", "board", "board__community").filter(id=review_id).first()
    if review is None:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(ReviewSerializer(review).data, status=status.HTTP_200_OK)

    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    if review.user_id != request.user.id:
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "DELETE":
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PATCH (rating/content만 허용)
    data = request.data if isinstance(request.data, dict) else {}
    rating = data.get("rating")
    content = data.get("content")

    if rating is not None:
        try:
            rating_int = int(rating)
        except Exception:
            return Response({"error": "rating must be int"}, status=status.HTTP_400_BAD_REQUEST)
        if rating_int < 1 or rating_int > 5:
            return Response({"error": "rating must be 1~5"}, status=status.HTTP_400_BAD_REQUEST)
        review.rating = rating_int

    if content is not None:
        review.content = content

    review.save()
    return Response(ReviewSerializer(review).data, status=status.HTTP_200_OK)


# ---------- COMMENTS (Post / Review) ----------
def _comment_list_create(request, target_obj):
    if request.method == "GET":
        ct = ContentType.objects.get_for_model(target_obj.__class__)
        qs = Comment.objects.filter(content_type=ct, object_id=target_obj.id).select_related("user")
        return Response(CommentSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = CommentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ct = ContentType.objects.get_for_model(target_obj.__class__)
    comment = Comment.objects.create(
        user=request.user,
        content=serializer.validated_data["content"],
        content_type=ct,
        object_id=target_obj.id,
    )
    return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
def post_comments(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    if post is None:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    return _comment_list_create(request, post)


@api_view(["GET", "POST"])
def review_comments(request, review_id):
    review = Review.objects.filter(id=review_id).first()
    if review is None:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
    return _comment_list_create(request, review)
