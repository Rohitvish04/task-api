from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ("ADMIN", "Admin"),
    ("MANAGER", "Manager"),
    ("USER", "User"),
)


class User(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")

    # only used when role=USER, points at the manager this person reports to
    manager = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="team"
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
