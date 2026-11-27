
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import MediaItem, MediaType, UserMedia

User = get_user_model()


class CatalogFeatureTests(TestCase):

    def setUp(self):
        # Create two separate users
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPass123!"
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="TestPass123!"
        )

        # Create a media type
        self.media_type = MediaType.objects.create(
            type_name="Game"
        )

        # Create a sample media item
        self.media = MediaItem.objects.create(
            media_type=self.media_type,
            title="Test Game",
            description="A test game.",
            release_date=timezone.now(),
            created_by=self.user
        )

    def test_add_media_valid(self):
        """Valid media information creates a media record."""
        self.client.login(
            username="testuser",
            password="TestPass123!"
        )

        response = self.client.post(
            reverse("catalog:add_media"),
            {
                "media_type": self.media_type.id,
                "title": "New Test Game",
                "description": "Another test game.",
                "release_date": "2025-01-01"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            MediaItem.objects.filter(title="New Test Game").exists()
        )

    def test_add_media_invalid(self):
        """Missing required media information is rejected."""
        self.client.login(
            username="testuser",
            password="TestPass123!"
        )

        response = self.client.post(
            reverse("catalog:add_media"),
            {
                "media_type": self.media_type.id,
                "title": "",
                "description": "Missing title.",
                "release_date": "2025-01-01"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            MediaItem.objects.filter(title="").exists()
        )

    def test_my_backlog_requires_login(self):
        """Anonymous users cannot access their personal backlog."""
        response = self.client.get(
            reverse("catalog:my_backlog")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_cannot_update_other_users_backlog_entry(self):
        """Users cannot update another user's backlog entry."""
        entry = UserMedia.objects.create(
            user=self.other_user,
            media=self.media
        )

        self.client.login(
            username="testuser",
            password="TestPass123!"
        )

        response = self.client.post(
            reverse(
                "catalog:update_backlog_status",
                args=[entry.id]
            ),
            {"status": UserMedia.Status.COMPLETED}
        )

        self.assertEqual(response.status_code, 404)

        entry.refresh_from_db()
        self.assertEqual(
            entry.status,
            UserMedia.Status.WISHLISTED
        )

    def test_add_to_backlog_valid(self):
        """A user can add media to their personal backlog."""
        self.client.login(
            username="testuser",
            password="TestPass123!"
        )

        response = self.client.post(
            reverse(
                "catalog:add_to_backlog",
                args=[self.media.id]
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            UserMedia.objects.filter(
                user=self.user,
                media=self.media
            ).exists()
        )

    def test_add_to_backlog_prevents_duplicates(self):
        """Adding the same media twice does not create duplicates."""
        self.client.login(
            username="testuser",
            password="TestPass123!"
        )

        url = reverse(
            "catalog:add_to_backlog",
            args=[self.media.id]
        )

        self.client.post(url)
        self.client.post(url)

        self.assertEqual(
            UserMedia.objects.filter(
                user=self.user,
                media=self.media
            ).count(),
            1
        )

    def test_update_backlog_status_valid(self):
        """A user can update their own backlog status."""
        entry = UserMedia.objects.create(
            user=self.user,
            media=self.media
        )

        self.client.login(
            username="testuser",
            password="TestPass123!"
        )

        response = self.client.post(
            reverse(
                "catalog:update_backlog_status",
                args=[entry.id]
            ),
            {"status": UserMedia.Status.COMPLETED}
        )

        self.assertEqual(response.status_code, 302)

        entry.refresh_from_db()
        self.assertEqual(
            entry.status,
            UserMedia.Status.COMPLETED
        )

    def test_remove_from_backlog(self):
        """A user can remove an item from their own backlog."""
        entry = UserMedia.objects.create(
            user=self.user,
            media=self.media
        )

        self.client.login(
            username="testuser",
            password="TestPass123!"
        )

        response = self.client.post(
            reverse(
                "catalog:remove_from_backlog",
                args=[entry.id]
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            UserMedia.objects.filter(id=entry.id).exists()
        )


    def test_edit_media_valid(self):
        """An authorized user can edit their own media."""
        self.client.login(
            username="testuser",
            password="TestPass123!"
        )

        response = self.client.post(
            reverse("catalog:edit_media", args=[self.media.id]),
            {
                "media_type": self.media_type.id,
                "title": "Updated Test Game",
                "description": "Updated description.",
                "release_date": "2025-01-01"
            }
        )

        self.assertEqual(response.status_code, 302)

        self.media.refresh_from_db()
        self.assertEqual(self.media.title, "Updated Test Game")

    def test_cannot_edit_another_users_media(self):
        """A user cannot edit media submitted by another user."""
        self.media.created_by = self.other_user
        self.media.save()

        self.client.login(
            username="testuser",
            password="TestPass123!"
        )

        response = self.client.post(
            reverse("catalog:edit_media", args=[self.media.id]),
            {
                "media_type": self.media_type.id,
                "title": "Unauthorized Edit",
                "description": "Should not be saved.",
                "release_date": "2025-01-01"
            }
        )

        self.assertEqual(response.status_code, 302)

        self.media.refresh_from_db()
        self.assertEqual(self.media.title, "Test Game")

    def test_delete_media_valid(self):
        """An authorized user can delete their own media."""
        self.client.login(
            username="testuser",
            password="TestPass123!"
        )

        response = self.client.post(
            reverse("catalog:delete_media", args=[self.media.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            MediaItem.objects.filter(id=self.media.id).exists()
        )

    def test_update_backlog_status_invalid(self):
        """An invalid backlog status is rejected."""
        entry = UserMedia.objects.create(
            user=self.user,
            media=self.media
        )

        self.client.login(
            username="testuser",
            password="TestPass123!"
        )

        response = self.client.post(
            reverse(
                "catalog:update_backlog_status",
                args=[entry.id]
            ),
            {"status": "INVALID_STATUS"}
        )

        self.assertEqual(response.status_code, 302)

        entry.refresh_from_db()
        self.assertEqual(
            entry.status,
            UserMedia.Status.WISHLISTED
        )
