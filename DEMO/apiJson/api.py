# myapp/api.py
from django.contrib.auth.models import User
from social.apps.django_app.default.models import UserSocialAuth
from tastypie import fields
from tastypie.resources import ModelResource

from django.contrib.auth import *
from django.http import HttpResponse


def build_content_type(format, encoding='utf-8'):
    """
    Appends character encoding to the provided format if not already present.
    """
    if 'charset' in format:
        return format

    return "%s; charset=%s" % (format, encoding)

class MyModelResource(ModelResource):
    def create_response(self, request, data, response_class=HttpResponse, **response_kwargs):
        """
        Extracts the common "which-format/serialize/return-response" cycle.

        Mostly a useful shortcut/hook.
        """
        desired_format = self.determine_format(request)
        serialized = self.serialize(request, data, desired_format)
        return response_class(content=serialized, content_type=build_content_type(desired_format), **response_kwargs)

class UserResource(MyModelResource):
	
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        # fields = ['id','username', 'first_name', 'last_name','email', 'last_login','date_joined','password','resource_uri']
        


class UserSocialAuthResource(MyModelResource):
	"""docstring for UserSocialAuthResource"""
	user_id = fields.ForeignKey(UserResource, 'user')
	class Meta:
		queryset = UserSocialAuth.objects.all()
		resource_name = 'social'
		