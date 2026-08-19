from django.conf import settings
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    done = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
