from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ("ADMIN", "Admin"),
    ("MANAGER", "Manager"),
    ("USER", "User"),
)


class User(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")

    # didn't want a separate Team table for this - a User just points at
    # whoever their Manager is. only makes sense when role=USER
    manager = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="team"
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
