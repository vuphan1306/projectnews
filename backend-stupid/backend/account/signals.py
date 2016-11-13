"""All image handlers."""

from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from tastypie.models import create_api_key
from .models import UserProfile

models.signals.post_save.connect(create_api_key, sender=User)


@receiver(models.signals.post_delete, sender=UserProfile)
def delete_userprofile(sender, **kwargs):
    """Delete user profile."""
    try:
        userprofile = kwargs["instance"]
        User.objects.filter(id=userprofile.user.id).delete()
    except ValueError as e:
        print('delete_userprofile %s' % e)
        pass
