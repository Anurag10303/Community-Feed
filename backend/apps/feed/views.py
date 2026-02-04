from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .services import like_post
from .selectors import get_comment_tree, get_leaderboard_last_24h


# ===================== HELPERS =====================

def get_user_from_request(request):
    """
    Temporary user resolution (NO AUTH).
    Accepts:
    - ?user_id=<id> (GET)
    - { user_id: <id> } (POST)

    Automatically creates user if missing.
    """

    user_id = (
        request.query_params.get("user_id")
        or request.data.get("user_id")
    )

    if not user_id:
        return None

    user, _ = User.objects.get_or_create(
        id=user_id,
        defaults={"username": f"user_{user_id}"}
    )
    return user


# ===================== FEED =====================

class FeedListAPIView(APIView):
    """
    GET /api/feed/?user_id=1
    """

    def get(self, request):
        posts = (
            Post.objects
            .select_related("author")
            .prefetch_related("likes", "comments")
            .order_by("-created_at")
        )

        serializer = PostSerializer(
            posts,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDetailAPIView(APIView):
    """
    GET /api/feed/<post_id>/?user_id=1
    """

    def get(self, request, post_id: int):
        post = get_object_or_404(
            Post.objects
            .select_related("author")
            .prefetch_related("likes", "comments"),
            id=post_id
        )

        comment_tree = get_comment_tree(post_id=post.id)

        post_data = PostSerializer(
            post,
            context={"request": request}
        ).data

        post_data["comments"] = CommentSerializer(
            comment_tree,
            many=True
        ).data

        return Response(post_data, status=status.HTTP_200_OK)


# ===================== LIKES =====================

class LikePostAPIView(APIView):
    """
    POST /api/feed/<post_id>/like/
    body: { "user_id": 1 }
    """

    def post(self, request, post_id: int):
        user = get_user_from_request(request)
        if not user:
            return Response(
                {"detail": "user_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        post = get_object_or_404(Post, id=post_id)

        created = like_post(user=user, post=post)

        if not created:
            return Response(
                {"detail": "Already liked"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "Post liked"},
            status=status.HTTP_201_CREATED
        )


# ===================== COMMENTS =====================

class AddCommentAPIView(APIView):
    """
    POST /api/feed/<post_id>/comment/
    body: { "content": "...", "parent_id": null, "user_id": 1 }
    """

    def post(self, request, post_id: int):
        user = get_user_from_request(request)
        if not user:
            return Response(
                {"detail": "user_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        content = request.data.get("content")
        parent_id = request.data.get("parent_id")

        if not content:
            return Response(
                {"detail": "content required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        post = get_object_or_404(Post, id=post_id)

        Comment.objects.create(
            post=post,
            author=user,
            content=content,
            parent_id=parent_id
        )

        return Response(
            {"detail": "Comment added"},
            status=status.HTTP_201_CREATED
        )


# ===================== LEADERBOARD =====================

class LeaderboardAPIView(APIView):
    """
    GET /api/feed/leaderboard/
    """

    def get(self, request):
        leaderboard = get_leaderboard_last_24h(limit=5)
        return Response(leaderboard, status=status.HTTP_200_OK)

class LikeCommentAPIView(APIView):
    """
    POST /api/comments/<comment_id>/like/
    body: { "user_id": 1 }
    """

    def post(self, request, comment_id: int):
        user = get_user_from_request(request)
        if not user:
            return Response(
                {"detail": "user_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        comment = get_object_or_404(Comment, id=comment_id)

        from .services import like_comment
        created = like_comment(user=user, comment=comment)

        if not created:
            return Response(
                {"detail": "Already liked"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "Comment liked"},
            status=status.HTTP_201_CREATED
        )
