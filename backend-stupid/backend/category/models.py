"""Message model."""
from django.db import models
from django.conf import settings
from backend.commons.models import TimeStampedModel


class Category(TimeStampedModel):
    """Description: Model Description."""

    name = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             null=True, blank=True)
    display_order = models.IntegerField(default=0)
    status_code = models.IntegerField(default=0, null=False)

    def __str__(self):
        """String display func."""
        return self.name
