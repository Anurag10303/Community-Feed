from django.db import IntegrityError, transaction
from .models import Like, KarmaEvent

def like_comment(*, user, comment):
    """
    Returns True if like was created, False if already liked
    """
    if Like.objects.filter(user=user, comment=comment).exists():
        return False

    with transaction.atomic():
        Like.objects.create(
            user=user,
            comment=comment
        )

        # +1 karma to comment author
        KarmaEvent.objects.create(
            user=comment.author,
            points=1
        )

    return True

def like_post(*, user, post):
    """
    Returns True if like was created, False if already liked.
    Adds +5 karma ONLY on first like.
    """
    try:
        with transaction.atomic():
            Like.objects.create(user=user, post=post)

            KarmaEvent.objects.create(
                user=post.author,
                points=5
            )

        return True

    except IntegrityError:
        # unique_user_post_like violated
        return False


def like_comment(*, user, comment):
    """
    Returns True if like was created, False if already liked.
    Adds +1 karma ONLY on first like.
    """
    try:
        with transaction.atomic():
            Like.objects.create(user=user, comment=comment)

            KarmaEvent.objects.create(
                user=comment.author,
                points=1
            )

        return True

    except IntegrityError:
        return False
