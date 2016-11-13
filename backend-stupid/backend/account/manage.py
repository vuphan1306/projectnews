"""Manage user profile api."""
from django.db import models


class UserProfileQuerySet(models.Model):
    """User profile query set, that contains all query set of user profile."""

    def get_user_by_email(self, email):
        """Get user by email."""
        return self.filter(user_email=email)

    def get_user_by_email_password(self, email, passwd):
        """Get user by email and password."""
        return self.filter(user_email=email, user_password=passwd)


class UserProfileManager(models.Model):
    """Manage all query set."""

    def get_query_set(self):
        """Get all profile query set."""
        return UserProfileQuerySet(self.model, using=self._db)

    def get_user_by_email(self, email):
        """Get user by email."""
        return self.get_query_set().get_user_by_email(email)

    def get_user_by_email_password(self, email, passwd):
        """Get user by email and password."""
        return self.get_query_set().get_user_by_email_password(email, passwd)
