"""All account apis will be defined here."""

from __future__ import absolute_import
from .models import Comment # noqa
from ..commons.authentication import AccessTokenAuthentication
from tastypie.resources import ModelResource
from backend.authorization.custom_authorization import NoAccessAuthorization
from ..account.models import UserProfile
from ..commons.custom_exception import CustomBadRequest
from tastypie.validation import Validation
from django.conf.urls import url
from tastypie.utils import trailing_slash, timezone
from ..commons.datetime_utils import convert_utc_time_to_local_time
from django.contrib.contenttypes.models import ContentType
from ..article.models import Article


class CommentValidation(Validation):
    """Provide helper function to validation data when create article or Style."""

    def is_valid(self, bundle, request=None):
        """Helper function to check bundle data valid or not valid."""
        if not bundle:
            return {'__all__': 'Input data not found!'}

        errors = {}
        if 'comment_id' not in bundle:
            errors["comment_id"] = ['You must enter comment_id.']
        if 'text' not in bundle:
            errors["text"] = ['You must enter text.']
        return errors


class CommentResource(ModelResource):
    """Review resource."""

    class Meta(object):
        """ReviewResource Meta data."""

        allowed_methods = ['get', 'post', 'delete', 'put']
        fields = ['user', 'article', 'text', 'created', 'id']
        include_resource_uri = False
        always_return_data = True
        authentication = AccessTokenAuthentication()
        authorization = NoAccessAuthorization()
        queryset = Comment.objects.all()  # noqa
        resource_name = 'comment'

    def prepend_urls(self):
        """Api urls."""
        return [
            url(r"^(?P<resource_name>%s)/get_article_comments%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_article_comments'), name="api_get_article_comments"),
            url(r"^(?P<resource_name>%s)/update_comment%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('update_comment'), name="api_update_comment"),
            url(r"^(?P<resource_name>%s)/delete_comment%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('delete_comment'), name="api_delete_comment"),
        ]

    def dehydrate(self, bundle):
        """Tastypie dehydrate method."""
        bundle.data['user'] = {
            'id': bundle.obj.user.id,
            'name': bundle.obj.user.first_name + " " + bundle.obj.user.last_name
        }
        # Get user avatar
        try:
            user_profile = UserProfile.objects.get(user=bundle.obj.user)
            bundle.data['user']['user_avatar'] = user_profile.image
        except UserProfile.DoesNotExist:
            raise CustomBadRequest(
                error_type='UNAUTHORIZED', error_message='User profile not found!')
        # Convert utc time to local time.
        bundle.data['created'] = convert_utc_time_to_local_time(bundle.obj.created)
        return bundle

    def create(self, **kwargs):
        """Provide helper function to create comment resource."""
        # Get all relationship question of this product
        print(kwargs)

        comment = Comment.objects.create(
            text=kwargs['text'],
            article_id=kwargs['article_id'],
            user_id=kwargs['user_id'],
            created=timezone.now(),
            modified=timezone.now())
        # print('user_id: ', kwargs['request'])

        bundle = self.build_bundle(request=kwargs['request'], obj=comment)
        bundle = self.full_dehydrate(bundle)

        return bundle

    def update(self, request, data):
        """Provide helper function to update comment resource."""
        # Check validation data
        validation = CommentValidation()
        errors = validation.is_valid(data)
        if errors:
            raise CustomBadRequest(error_type='INVALID_DATA',
                                   error_message=errors)
        comment_id = data.get('comment_id')
        text = data.get('text')
        try:
            comment = Comment.objects.get(pk=comment_id)
            if request.user.id == comment.user.id:
                comment.text = text
                comment.save()
            else:
                raise CustomBadRequest(
                    error_type='UNAUTHORIZED',
                    error_message='Permission denied!')
        except Comment.DoesNotExist:
            raise CustomBadRequest(
                error_type='INVALID_DATA',
                error_message='Comment does not exist!')

        bundle = self.build_bundle(request=request, obj=comment)
        bundle = self.full_dehydrate(bundle)

        return bundle

    def delete(self, request, data):
        """Provide helper function to delete comment resource."""
        # Get all relationship question of this product
        comment_id = data.get('comment_id', None)
        if comment_id is not None:
            comment = Comment.objects.get(pk=comment_id)
            if request.user.id == comment.user.id:
                comment.delete()
            else:
                raise CustomBadRequest(
                    error_type='UNAUTHORIZED',
                    error_message='Permission denied!')
        else:
            raise CustomBadRequest(
                error_type='MISSING_PARAMATER',
                error_message='You must enter comment id!')

    def get_last_comment(self, object_content, **kwargs):
        """Provide helper function to get all comment of object_content."""
        comments = Comment.objects.all()

        data = None
        if len(comments):
            comment = comments.first()
            bundle = self.build_bundle(request=kwargs['request'], obj=comment)
            bundle = self.full_dehydrate(bundle)

            data = {
                'total_comments': len(comments),
                'lastest_comment': bundle
            }

        return data

    def get_comments(self, object_content, **kwargs):
        """Provide helper function to get all comment of object_content."""
        contenttype_obj = ContentType.objects.get_for_model(object_content)
        # Get all relationship question of this product
        comments = Comment.objects.filter(
            object_type=contenttype_obj,
            object_id=object_content.id)

        comments_bundles = []
        for comment in comments:
            bundle = self.build_bundle(request=kwargs['request'], obj=comment)
            bundle = self.full_dehydrate(bundle)
            comments_bundles.append(bundle)

        return comments_bundles

    def update_comment(self, request, **kwargs):
        """Provide api to update a comment."""
        self.method_check(request, allowed=['post'])
        self._meta.authentication.is_authenticated(request)
        self.throttle_check(request)
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))
        bundle = self.update(request, data)
        return self.create_response(request, bundle)

    def delete_comment(self, request, **kwargs):
        """Provide api to update a comment."""
        self.method_check(request, allowed=['delete'])
        self._meta.authentication.is_authenticated(request)
        self.throttle_check(request)
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))
        self.delete(request, data)
        return self.create_response(request, {"Success": True})

    def get_article_comments(self, request, **kwargs):
        """Provide api to get all comment of a article with id."""
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        article_id = request.GET.get('id', None)
        if article_id is not None:
            try:
                # Get question with this id.
                article = Article.objects.get(pk=article_id)
                comments = Comment.objects.filter(
                    article=article.id)

                return self.paginator(request, comments)
            except Article.DoesNotExist:
                raise CustomBadRequest(error_type="INVALID_DATA", error_message='Article does not exist!')
        else:
            raise CustomBadRequest(error_type="INVALID_DATA", error_message='You must enter id of article!')

    def paginator(self, request, objects, **kwargs):
        """Helper function to paginator result list."""
        paginator = self._meta.paginator_class(
            request.GET, objects, resource_uri=self.get_resource_uri(),
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
