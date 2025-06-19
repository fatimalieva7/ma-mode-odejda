

from django.utils import timezone
from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"