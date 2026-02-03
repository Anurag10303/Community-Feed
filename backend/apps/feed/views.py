from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .services import like_post, like_comment
from .selectors import get_comment_tree

from .selectors import get_leaderboard_last_24h

class FeedListAPIView(APIView):
    """
    GET /api/feed/
    Returns list of posts (no comments).
    """

    def get(self, request):
        posts = (
            Post.objects
            .select_related("author")
            .order_by("-created_at")
        )

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostDetailAPIView(APIView):
    """
    GET /api/feed/<post_id>/
    Returns single post with threaded comments.
    """

    def get(self, request, post_id: int):
        post = get_object_or_404(
            Post.objects.select_related("author"),
            id=post_id
        )

        comment_tree = get_comment_tree(post_id=post.id)

        post_data = PostSerializer(post).data
        post_data["comments"] = CommentSerializer(
            comment_tree,
            many=True
        ).data

        return Response(post_data, status=status.HTTP_200_OK)

class LikePostAPIView(APIView):
    """
    POST /api/feed/<post_id>/like/
    """

    def post(self, request, post_id: int):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        post = get_object_or_404(Post, id=post_id)

        created = like_post(user=request.user, post=post)

        if not created:
            return Response(
                {"detail": "Already liked"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "Post liked"},
            status=status.HTTP_201_CREATED
        )

class LikeCommentAPIView(APIView):
    """
    POST /api/comments/<comment_id>/like/
    """

    def post(self, request, comment_id: int):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        comment = get_object_or_404(Comment, id=comment_id)

        created = like_comment(user=request.user, comment=comment)

        if not created:
            return Response(
                {"detail": "Already liked"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "Comment liked"},
            status=status.HTTP_201_CREATED
        )

class LeaderboardAPIView(APIView):
    """
    GET /api/feed/leaderboard/
    Returns top 5 users by karma earned in last 24 hours.
    """

    def get(self, request):
        leaderboard = get_leaderboard_last_24h(limit=5)
        return Response(leaderboard, status=status.HTTP_200_OK)
