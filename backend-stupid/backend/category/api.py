"""All account apis will be defined here."""

from __future__ import absolute_import
from ..commons.authentication import AccessTokenAuthentication
from tastypie.resources import ModelResource
from ..commons.custom_exception import CustomBadRequest
from tastypie.authorization import DjangoAuthorization
from tastypie.validation import Validation
from django.contrib.auth.models import User
from tastypie.utils import trailing_slash, timezone
from .models import Category
from django.conf.urls import url


class CategoryValidation(Validation):
    """Provide helper function to validation data when create category or Style."""

    def is_valid(self, bundle, request=None):
        """Check validation."""
        if not bundle.data:
            return {'__all__': 'Request name and description paramaters.'}

        errors = {}
        if 'name' not in bundle.data:
            errors["name"] = ['You must enter name.']
        # if 'description' not in bundle.data:
        #     errors["description"] = ['You must enter description.']
        return errors


class CategoryResource(ModelResource):
    """Category resource."""

    class Meta(object):
        """CategoryResource Meta data."""

        allowed_methods = {'get', 'post'}
        always_return_data = True
        authentication = AccessTokenAuthentication()
        authorization = DjangoAuthorization()
        validation = CategoryValidation()
        queryset = Category.objects.all() # noqa
        resource_name = 'category'
        filtering = {
            'id': ['exact'],
        }

    def dehydrate(self, bundle):
        """Tastypie dehydrate method."""
        category = Category.objects.get(id=bundle.obj.id) # noqa
        if category.user is not None:
            bundle.data['user'] = category.user.id
        else:
            bundle.data['user'] = ''

        return super(CategoryResource, self).dehydrate(bundle)

    def prepend_urls(self):
        """Api urls."""
        return [
            url(r"^(?P<resource_name>%s)/create%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('create'), name="api_create"),
            url(r"^(?P<resource_name>%s)/update%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('update'), name="api_update_category"),
            url(r"^(?P<resource_name>%s)/get_all%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_all'), name="api_get_all"),
            url(r"^(?P<resource_name>%s)/delete%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('delete'), name="api_delete"),
        ]

    def create(self, request, **kwargs):
        """Provide helper function to create comment resource."""
        # Get all relationship question of this product
        self.method_check(request, allowed=['post'])
        self.throttle_check(request)
        self._meta.authentication.is_authenticated(request)
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))
        request_bundle = self.build_bundle(request=request)
        request_bundle.data = data
        name = data.get('name', None)
        display_order = data.get('display_order', 0)
        status_code = data.get('status_code', 1)
        user = request.user.id
        print('user', user)
        try:
            Category.objects.create(
                name=name,
                display_order=display_order,
                user_id=user,
                status_code=status_code,
                created=timezone.now(),
                modified=timezone.now())
            return self.create_response(request, {"Success": True})
        except User.DoesNotExist:
                    raise CustomBadRequest(error_type='INVALID_DATA', error_message='Cant find receiver user with id!')

    def update(self, request, **kwargs):
        """Provide helper function to create comment resource."""
        # Get all relationship question of this product
        self.method_check(request, allowed=['post'])
        self.throttle_check(request)
        self._meta.authentication.is_authenticated(request)
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))
        request_bundle = self.build_bundle(request=request)
        request_bundle.data = data
        name = data.get('name', None)
        display_order = data.get('display_order', 0)
        status_code = data.get('status_code', 1)
        category_id = data.get('id', None)
        user = request.user.id
        print('user', user)
        try:
            obj = Category.objects.get(id=category_id)
            obj.name = name
            obj.display_order = display_order
            obj.status_code = status_code
            obj.save()
            return self.create_response(request, {'Update success': True})
        except User.DoesNotExist:
                    raise CustomBadRequest(error_type='INVALID_DATA', error_message='Cant find receiver user with id!')

    def get_all(self, request, **kwargs):
        """Provide api to get all styles with specify organize."""
        # self.method_check(request, allowed=['get'])
        # self.throttle_check(request)
        # category = Category.objects.all().order_by('display_order')
        # bundle = category
        # return self.create_response(request, bundle)
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        parent_objs = Category.objects.order_by('display_order')
        bundle = self.build_bundle(request=request)
        bundle.data['objects'] = []
        for category in parent_objs:
            self.add_info(request, bundle.data['objects'], category)
        return self.create_response(request, bundle)

    def delete(self, request, **kwargs):
        """Provide api to delete category."""
        # self.method_check(request, allowed=['post'])
        self.throttle_check(request)
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))
        self._meta.authentication.is_authenticated(request)
        bundle = self.build_bundle(request=request)
        category_id = data.get('id', None)

        try:
            bundle.obj = Category.objects.get(pk=category_id)
            # self.authorized_delete_detail(self.get_object_list(bundle.request), bundle)
            delete_number, objects = Category.objects.filter(pk=category_id).delete()
            return self.create_response(request, {'success': True, 'deleted': delete_number})
        except Category.DoesNotExist:
            raise CustomBadRequest(error_type='INVALID_DATA', error_message='Dont match any category with above id')

    def add_info(self, request, list_data, category):
        """add_info."""
        data = {
            'id': category.id,
            'name': category.name,
            'status_code': category.status_code,
            'display_order': category.display_order
        }
        list_data.append(data)
