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
from ..category.models import Category
from haystack.query import SearchQuerySet
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

    ARTICLE = 'Article'

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
        if article.create_by is not None:
            bundle.data['user'] = article.create_by.id
        else:
            bundle.data['user'] = ''
        if article.category is not None:
            bundle.data['category'] = article.category.id
        else:
            bundle.data['category'] = ''
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
            url(r"^(?P<resource_name>%s)/get_top_news_by_category%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_top_news_by_category'), name="api_get_top_news_by_category"),
            url(r"^(?P<resource_name>%s)/get_top_news%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_top_news'), name="api_get_top_news"),
            url(r"^(?P<resource_name>%s)/get_all%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_all'), name="api_get_all"),
            url(r"^(?P<resource_name>%s)/delete%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('delete'), name="api_delete"),
            url(r"^(?P<resource_name>%s)/article_search%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('article_search'), name="api_article_search"),
            url(r"^(?P<resource_name>%s)/get_detail_by_article_id%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_detail_by_article_id'), name="api_get_detail_by_article_id"),
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
        image_url = data.get('image_url', 'assets/img/news/h1.jpg')
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
                image_url=image_url,
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
        image_url = data.get('image_url', 'assets/img/news/h1.jpg')
        try:
            obj = Article.objects.get(id=article_id)
            obj.title = title
            obj.content = content
            obj.description = description
            obj.category_id = category_id
            obj.display_order = display_order
            obj.status_code = status_code
            obj.create_by_id = user
            obj.image_url = image_url
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

    def get_detail_by_article_id(self, request, **kwargs):
        """Provide api to get top news article of a category with id."""
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        article_id = request.GET.get('id', None)
        if article_id is not None:
            try:
                # Get question with this id.
                article = Article.objects.get(pk=article_id)
                articles = Article.objects.filter(
                    id=article.id)

                return self.paginator(request, articles)
            except Category.DoesNotExist:
                raise CustomBadRequest(error_type="INVALID_DATA", error_message='Category does not exist!')
        else:
            raise CustomBadRequest(error_type="INVALID_DATA", error_message='You must enter id of category!')

    def get_top_news_by_category(self, request, **kwargs):
        """Provide api to get top news article of a category with id."""
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        category_id = request.GET.get('id', None)
        if category_id is not None:
            try:
                # Get question with this id.
                category = Category.objects.get(pk=category_id)
                articles = Article.objects.filter(
                    category=category.id)

                return self.paginator(request, articles)
            except Category.DoesNotExist:
                raise CustomBadRequest(error_type="INVALID_DATA", error_message='Category does not exist!')
        else:
            raise CustomBadRequest(error_type="INVALID_DATA", error_message='You must enter id of category!')

    def get_top_news(self, request, **kwargs):
        """Provide api to get top news article of a category with id."""
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        try:
            # Get question with this id.
            articles = Article.objects.all()

            return self.paginator(request, articles)
        except Category.DoesNotExist:
            raise CustomBadRequest(error_type="INVALID_DATA", error_message='Category does not exist!')

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
            'display_order': article.display_order,
            'image_url': article.image_url
        }
        list_data.append(data)

    def paginator(self, request, objects, **kwargs):
        """Helper function to paginator result list."""
        paginator = self._meta.paginator_class(
            request.GET, objects, resource_uri=self.get_resource_uri() + 'get_top_news_by_category',
            limit=self._meta.limit, max_limit=self._meta.max_limit,
            collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = [
            self.full_dehydrate(self.build_bundle(obj=obj, request=request), for_list=True)
            for obj in to_be_serialized[self._meta.collection_name]
        ]

        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized)

    def article_search(self, request, **kwargs):
        """Search api."""
        self.method_check(request, allowed=['get'])
        self._meta.authentication.is_authenticated(request)
        self.throttle_check(request)

        q = str(request.GET.get('q', ''))

        sqs = SearchQuerySet().models(Article).load_all().filter(content=q, product_type=self.ARTICLE)

        return self.search_paginator(request, sqs)

    def search_paginator(self, request, sqs):
        """Helper function to paginator results."""
        from django.core.paginator import Paginator
        # Do the query.
        page_number = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        paginator = Paginator(sqs, limit)

        try:
            page = paginator.page(page_number)
        except Exception:
            raise CustomBadRequest(error_type='INVALID_DATA', error_message='Sorry, no results on that page.')

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
            'meta': {
                'total': paginator.count,
                'page': page_number,
                'limit': limit
            }
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)
