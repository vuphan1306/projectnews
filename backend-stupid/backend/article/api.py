"""All account apis will be defined here."""

from __future__ import absolute_import
from ..commons.authentication import AccessTokenAuthentication
from tastypie.resources import ModelResource
from ..commons.custom_exception import CustomBadRequest
from tastypie.authorization import DjangoAuthorization
from tastypie.validation import Validation
from django.contrib.auth.models import User
from tastypie.utils import trailing_slash, timezone
from ..comment.api import CommentResource
from ..commons.datetime_utils import convert_utc_time_to_local_time
from .models import Article
from django.conf.urls import url


class ArticleValidation(Validation):
    """Provide helper function to validation data when create article or Style."""

    def is_valid(self, bundle, request=None):
        """Check validation."""
        if not bundle.data:
            return {'__all__': 'Request title, content and description paramaters.'}

        errors = {}
        if 'title' not in bundle.data:
            errors["title"] = ['You must enter title.']
        if 'description' not in bundle.data:
            errors["description"] = ['You must enter description.']
        if 'content' not in bundle.data:
            errors["title"] = ['You must enter content.']
        return errors


class ArticleResource(ModelResource):
    """Category resource."""

    class Meta(object):
        """CategoryResource Meta data."""

        allowed_methods = {'get', 'post'}
        always_return_data = True
        authentication = AccessTokenAuthentication()
        authorization = DjangoAuthorization()
        validation = ArticleValidation()
        queryset = Article.objects.all() # noqa
        resource_name = 'article'
        filtering = {
            'id': ['exact'],
        }

    def dehydrate(self, bundle):
        """Tastypie dehydrate method."""
        article = Article.objects.get(id=bundle.obj.id) # noqa
        if article.user is not None:
            bundle.data['user'] = article.user.id
        else:
            bundle.data['user'] = ''

        comment_resource = CommentResource()
        bundle.data['comments'] = comment_resource.get_last_comment(object_content=bundle.obj, request=bundle.request)

        # return super(ArticleResource, self).dehydrate(bundle)
        bundle.data['created'] = convert_utc_time_to_local_time(bundle.obj.created)
        return bundle

    def prepend_urls(self):
        """Api urls."""
        return [
            url(r"^(?P<resource_name>%s)/create%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('create'), name="api_create"),
            url(r"^(?P<resource_name>%s)/update%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('update'), name="api_update_article"),
            url(r"^(?P<resource_name>%s)/add_comment%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('add_comment'), name="api_add_comment"),
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
        title = data.get('title', None)
        content = data.get('content', None)
        description = data.get('description', None)
        category_id = data.get('category_id', None)
        display_order = data.get('display_order', 0)
        status_code = data.get('status_code', 1)
        user = request.user.id
        print('user', user)
        try:
            Article.objects.create(
                title=title,
                content=content,
                description=description,
                category_id=category_id,
                display_order=display_order,
                create_by_id=user,
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
        title = data.get('title', None)
        content = data.get('content', None)
        description = data.get('description', None)
        category_id = data.get('category_id', None)
        display_order = data.get('display_order', 0)
        status_code = data.get('status_code', 1)
        user = request.user.id
        article_id = data.get('id', None)
        try:
            obj = Article.objects.get(id=article_id)
            obj.title = title
            obj.content = content
            obj.description = description
            obj.category_id = category_id
            obj.display_order = display_order
            obj.status_code = status_code
            obj.create_by_id = user
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
        parent_objs = Article.objects.order_by('display_order')
        bundle = self.build_bundle(request=request)
        bundle.data['objects'] = []
        for article in parent_objs:
            self.add_info(request, bundle.data['objects'], article)
        return self.create_response(request, bundle)

    def delete(self, request, **kwargs):
        """Provide api to delete category."""
        # self.method_check(request, allowed=['post'])
        self.throttle_check(request)
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))
        self._meta.authentication.is_authenticated(request)
        bundle = self.build_bundle(request=request)
        article_id = data.get('id', None)

        try:
            bundle.obj = Article.objects.get(pk=article_id)
            # self.authorized_delete_detail(self.get_object_list(bundle.request), bundle)
            delete_number, objects = Article.objects.filter(pk=article_id).delete()
            return self.create_response(request, {'success': True, 'deleted': delete_number})
        except Article.DoesNotExist:
            raise CustomBadRequest(error_type='INVALID_DATA', error_message='Dont match any category with above id')

    def add_comment(self, request, **kwargs):
        """Provide api for create a question."""
        self.method_check(request, allowed=['post'])
        self._meta.authentication.is_authenticated(request)
        self.throttle_check(request)
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        article_id = data.get('article_id', None)
        # Get question
        try:
            article = Article.objects.get(pk=article_id)
            article.status_code = 1
            article.save()
        except Article.DoesNotExist:
            raise CustomBadRequest(error_type='INVALID_DATA',
                                   error_message="Article does not exist!")

        text = data.get('text', None)
        comment_resource = CommentResource()
        bundle = comment_resource.create(text=text, article_id=article_id, user_id=request.user.id, request=request)
        # bundle = self.build_bundle(request=request, obj=question)
        # bundle = self.full_dehydrate(bundle)

        return self.create_response(request, bundle)

    def add_info(self, request, list_data, article):
        """add_info."""
        data = {
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'description': article.description,
            'category_id': article.category_id,
            'create_by_id': article.create_by_id,
            'status_code': article.status_code,
            'display_order': article.display_order
        }
        list_data.append(data)
