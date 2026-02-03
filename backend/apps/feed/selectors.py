from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Sum

from .models import Comment, KarmaEvent

def get_comment_tree(*, post_id: int):
    """
    Returns a list of root comments.
    Each comment has a `.children` attribute populated in memory.
    """

    comments = (
        Comment.objects
        .filter(post_id=post_id)
        .select_related("author")
        .order_by("created_at")
    )

    comment_map = {}
    roots = []

    # First pass: initialize nodes
    for comment in comments:
        comment.children = []
        comment_map[comment.id] = comment

    # Second pass: attach children to parents
    for comment in comments:
        if comment.parent_id:
            parent = comment_map.get(comment.parent_id)
            if parent:
                parent.children.append(comment)
        else:
            roots.append(comment)

    return roots

def get_leaderboard_last_24h(limit: int = 5):
    """
    Returns top users by karma earned in the last 24 hours.
    """

    since = now() - timedelta(hours=24)

    leaderboard = (
        KarmaEvent.objects
        .filter(created_at__gte=since)
        .values("user_id", "user__username")
        .annotate(total_karma=Sum("points"))
        .order_by("-total_karma")[:limit]
    )

    return leaderboard
