from django.db import models
from django.conf import settings
# Create your models here.

class MediaType(models.Model):
    type_name = models.CharField(max_length=20, unique=True, null=False)

    def __str__(self):
        return self.type_name

class MediaItem(models.Model):
    media_type = models.ForeignKey(
        MediaType, on_delete=models.PROTECT,
        related_name="media_items"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_date = models.DateTimeField()
    cover_image = models.ImageField(
        upload_to="media_covers/",
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="submitted_media"
    )

class UserMedia(models.Model):
    class Status(models.TextChoices):
        WISHLISTED = "Wishlisted", "Wishlisted"
        IN_PROGRESS = "In Progress", "In Progress"
        ON_HOLD = "On Hold", "On Hold"
        DROPPED = "Dropped", "Dropped"
        COMPLETED = "Completed", "Completed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="backlog_entries"
    )
    media = models.ForeignKey(
            MediaItem,
            on_delete=models.CASCADE,
            related_name="backlog_entries"
        )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WISHLISTED
    )

    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=['user', 'media'],
                name='unique_user_media'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.media.title}"