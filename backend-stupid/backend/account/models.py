"""Define all account models."""

from __future__ import absolute_import
from django.db import models
from django.conf import settings
import uuid
import os
import sys
from ..commons.models import TimeStampedModel
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def get_unique_file_path(_, filename):
    """Get an unique file path with constant file upload prefix."""
    ext = filename.split('.')[1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(settings.FILE_UPLOAD_PREFIX_FOLDER_USER, filename)


class UserProfile(models.Model):
    """User profile models."""

    class Meta:
        """User profile meta data."""

        ordering = ['first_name']

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='userprofile', blank=True, null=True)
    status_code = models.SmallIntegerField(default=1)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    image_cover = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    date_last_update = models.DateField(null=True, blank=True)

    @property
    def full_name(self):
        """Custom full name method as a property."""
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        """Default string."""
        return self.user.email if self.user else ''


# class SellerCategory(TimeStampedModel):
#     """Seller category models."""

#     parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=100, null=True, blank=True)
#     display_order = models.IntegerField(default=0)
#     status_code = models.IntegerField(default=1)

#     def __str__(self):
#         """Default string."""
#         return self.name


# class Seller(models.Model):
#     """Seller profile models."""

#     user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='seller')
#     category = models.ForeignKey(SellerCategory, on_delete=models.CASCADE)
#     status_code = models.IntegerField(default=0)

#     # Not use yet fields.
#     license_number = models.CharField(max_length=100, null=True, blank=True)
#     certification_awards = models.CharField(max_length=400, null=True, blank=True)
#     affiliations = models.TextField(null=True, blank=True)
#     contact_post_code = models.CharField(max_length=10, null=True, blank=True)
#     additional_emails = models.CharField(max_length=400, null=True, blank=True)
#     date_last_update = models.DateField(auto_now_add=True, null=True, blank=True)

#     # Add customer fields
#     firm_name = models.CharField(max_length=100)
#     web_site = models.CharField(max_length=200, null=True, blank=True)
#     public_first_name = models.CharField(max_length=100, null=True, blank=True)
#     public_last_name = models.CharField(max_length=100, null=True, blank=True)
#     business_register_name = models.CharField(max_length=100, null=True, blank=True)
#     tax_number = models.CharField(max_length=30, null=True, blank=True)
#     legal_representative = models.CharField(max_length=100, null=True, blank=True)
#     contact_phone = models.CharField(max_length=15, null=True, blank=True)
#     contact_fax = models.CharField(max_length=15, null=True, blank=True)
#     business_description = models.TextField(null=True, blank=True)
#     service_provided = models.CharField(max_length=400, null=True, blank=True)
#     area_served = models.CharField(max_length=400, null=True, blank=True)
#     address = models.CharField(max_length=100, null=True, blank=True)

#     def __str__(self):
#         """Default string."""
#         return self.firm_name


class AccessToken(models.Model):
    """This class provide api for AccessToken."""

    access_token = models.UUIDField(default=uuid.uuid4, editable=False)
    device_type = models.CharField(max_length=10)
    access_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language_code = models.CharField(max_length=5)
    date_created = models.DateTimeField(auto_now_add=True)
    phone_token = models.CharField(max_length=200)
    phone_type = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        """Default string."""
        return str(self.access_token)


# class EmailVerification(models.Model):
#     """This class provide an Email Verification to verify email."""

#     token = models.UUIDField(default=uuid.uuid4, editable=False)
#     email = models.CharField(max_length=50)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_used = models.DateTimeField(blank=True, null=True)
#     is_expired = models.BooleanField(default=False)

#     def __str__(self):
#         """Docstring."""
#         return self.email


class LoginAccountType(models.Model):
    """Login accoune type model."""

    name = models.CharField(max_length=30, null=True)
    account_id = models.CharField(max_length=50, null=True)
    account_key = models.CharField(max_length=100, null=True)
    account_secret = models.CharField(max_length=100, null=True)
    request_permission = models.CharField(max_length=100, default='')

    def __str__(self):
        """Default string."""
        return str(self.name)


class UserLoginAccount(models.Model):
    """User login account model."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login_account_type = models.ForeignKey(LoginAccountType, on_delete=models.CASCADE)
    linked_user_id = models.CharField(max_length=30)
    access_token = models.CharField(max_length=100, null=True)
    granted_permissions = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_canceled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Default string."""
        return str(self.linked_user_id)
