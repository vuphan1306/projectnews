"""Custom authorization functions."""
from __future__ import absolute_import
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class UserObjectsOnlyAuthorization(Authorization):
    """User object only authorization."""

    def update_list(self, object_list, bundle):
        """Update list users."""
        raise Unauthorized("Sorry, no update by bundle.")

    def update_detail(self, object_list, bundle):
        """Update user details."""
        return bundle.obj.user == bundle.request.user.userprofile or bundle.request.user.is_superuser

    def delete_detail(self, object_list, bundle):
        """Delete user detail."""
        return bundle.obj.user == bundle.request.user.userprofile or bundle.request.user.is_superuser

    def delete_list(self, object_list, bundle):
        """Delete list users."""
        raise Unauthorized("Sorry, no deletes by bundle")

    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        if bundle.request.user.is_superuser:
            return object_list
        return object_list.filter(user=bundle.request.user)


class NoAccessAuthorization(Authorization):
    """User object only authorization."""

    def update_list(self, object_list, bundle):
        """Update list users."""    
        raise Unauthorized("Sorry, no update by bundle.")

    def update_detail(self, object_list, bundle):
        """Update user details."""
        raise Unauthorized("Sorry, no update by bundle.")

    def delete_detail(self, object_list, bundle):
        """Delete user detail."""
        raise Unauthorized("Sorry, no delete by bundle.")

    def delete_list(self, object_list, bundle):
        """Delete list users."""
        raise Unauthorized("Sorry, no deletes by bundle")

    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        raise Unauthorized("Sorry, no get by bundle.")