from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):

    class Role(models.TextChoices):
        USER = "USER", "User"
        ADMIN = "ADMIN", "Administrator"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)

    profile_photo = models.ImageField(
        upload_to="profile_photos/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username

