from django.urls import path
from .views import (
    FeedListAPIView,
    PostDetailAPIView,
    AddCommentAPIView,
    LikePostAPIView,
    LeaderboardAPIView,
    LikeCommentAPIView
)

urlpatterns = [
    path("feed/", FeedListAPIView.as_view()),
    path("feed/<int:post_id>/", PostDetailAPIView.as_view()),
    path("feed/<int:post_id>/comment/", AddCommentAPIView.as_view()),
    path("feed/<int:post_id>/like/", LikePostAPIView.as_view()),
    path("feed/leaderboard/", LeaderboardAPIView.as_view()),
    path("comments/<int:comment_id>/like/", LikeCommentAPIView.as_view()),
]

