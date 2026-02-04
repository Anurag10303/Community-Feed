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

from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum

from django.contrib.auth.models import User
from .models import KarmaEvent


def get_leaderboard_last_24h(limit=5):
    since = timezone.now() - timedelta(hours=24)

    qs = (
        KarmaEvent.objects
        .filter(created_at__gte=since)
        .values("user")
        .annotate(karma=Sum("points"))
        .order_by("-karma")[:limit]
    )

    # Convert to frontend-friendly shape
    result = []

    user_map = {
        u.id: u.username
        for u in User.objects.filter(id__in=[row["user"] for row in qs])
    }

    for row in qs:
        result.append({
            "user_id": row["user"],
            "username": user_map.get(row["user"], "unknown"),
            "karma": row["karma"],
        })

    return result

