from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now
from django.contrib.auth.models import User

from apps.feed.models import KarmaEvent
from apps.feed.selectors import get_leaderboard_last_24h


class LeaderboardLast24HoursTest(TestCase):
    def test_only_last_24_hours_karma_is_counted(self):
        """
        Karma older than 24 hours should be ignored.
        Karma within last 24 hours should be counted.
        """

        # Create users
        user_old = User.objects.create_user(username="old_user")
        user_new = User.objects.create_user(username="new_user")

        # Create old karma event (initially created with 'now')
        old_event = KarmaEvent.objects.create(
            user=user_old,
            points=100,
        )

        # Manually move old karma outside 24h window
        KarmaEvent.objects.filter(id=old_event.id).update(
            created_at=now() - timedelta(days=2)
        )

        # Create recent karma event (within last 24 hours)
        KarmaEvent.objects.create(
            user=user_new,
            points=10,
        )

        # Run leaderboard query
        leaderboard = get_leaderboard_last_24h(limit=5)

        # Assertions
        self.assertEqual(len(leaderboard), 1)
        self.assertEqual(leaderboard[0]["user__username"], "new_user")
        self.assertEqual(leaderboard[0]["total_karma"], 10)
