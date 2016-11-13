"""Message model."""
from django.db import models
from django.conf import settings
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
from backend.commons.models import TimeStampedModel
from ..category.models import Category


class Article(TimeStampedModel):
    """Description: Model Description."""

    class Meta:
        """Message meta data."""

        ordering = ['-created']
    title = models.CharField(max_length=100, default='Article')
    content = models.TextField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    display_order = models.IntegerField(default=0)
    status_code = models.IntegerField(default=0, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        """String display func."""
        return self.title
