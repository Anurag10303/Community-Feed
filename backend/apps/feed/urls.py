from django.urls import path
from .views import (
    FeedListAPIView,
    PostDetailAPIView,
    LikePostAPIView,
    LikeCommentAPIView,
    LeaderboardAPIView,
)

urlpatterns = [
    path("", FeedListAPIView.as_view(), name="feed-list"),
    path("leaderboard/", LeaderboardAPIView.as_view(), name="leaderboard"),
    path("<int:post_id>/", PostDetailAPIView.as_view(), name="post-detail"),
    path("<int:post_id>/like/", LikePostAPIView.as_view(), name="post-like"),
    path("comments/<int:comment_id>/like/", LikeCommentAPIView.as_view(), name="comment-like"),
]
