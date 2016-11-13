"""Message model."""
from django.db import models
from django.conf import settings
from backend.commons.models import TimeStampedModel
from ..article.models import Article


class Comment(TimeStampedModel):
    """Description: Model Description."""

    class Meta:
        """Message meta data."""

        ordering = ['-date_created']
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        """Default string."""
        return self.text
