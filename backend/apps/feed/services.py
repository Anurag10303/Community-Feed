from django.db import transaction, IntegrityError
from django.contrib.auth.models import User

from .models import Post, Comment, Like, KarmaEvent

@transaction.atomic
def like_post(*, user: User, post: Post) -> bool:
    """
    Returns True if like was created.
    Returns False if user already liked the post.
    """
    try:
        Like.objects.create(user=user, post=post)
        KarmaEvent.objects.create(user=post.author, points=5)
        return True
    except IntegrityError:
        # Unique constraint hit → already liked
        return False

@transaction.atomic
def like_comment(*, user: User, comment: Comment) -> bool:
    """
    Returns True if like was created.
    Returns False if user already liked the comment.
    """
    try:
        Like.objects.create(user=user, comment=comment)
        KarmaEvent.objects.create(user=comment.author, points=1)
        return True
    except IntegrityError:
        return False
