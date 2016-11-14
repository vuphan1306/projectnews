"""All account apis will be defined here."""

from __future__ import absolute_import
from django.contrib.auth import authenticate, login, logout
from django.conf.urls import url
from django.db import transaction
from django.utils import timezone
from .models import *  # noqa
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.http import HttpUnauthorized
from tastypie.utils import trailing_slash
from tastypie.models import ApiKey
from tastypie import fields
from tastypie.validation import Validation
from .signals import * # noqa
from .validation import UserProfileValidation
from ..commons.custom_exception import CustomBadRequest
from ..commons.multipart_resource import MultipartResource
from ..commons.authentication import ApiKeyAuthenticationExt, AccessTokenAuthentication
from ..authorization.custom_authorization import NoAccessAuthorization
from commons.email import send_email, send_email_reset_password


class InternalUserResource(ModelResource):
    """Internal user resource class."""

    class Meta(object):
        """Internal user resource meta data."""

        queryset = User.objects.all() # noqa
        excludes = ['password', 'is_superuser']
        resource_name = 'auth/users'
        authentication = ApiKeyAuthenticationExt()
        authorization = Authorization()


class UserResource(ModelResource):
    """User model resources."""

    class Meta(object):
        """User model resource meta data."""

        queryset = User.objects.all() # noqa
        fields = ['username', 'first_name', 'last_name', 'is_active']
        excludes = ['email', 'password', 'is_superuser']
        resource_name = 'auth/users'
        authentication = ApiKeyAuthenticationExt()
        authorization = Authorization()
        always_return_data = True


class InternalUserProfileResource(ModelResource):
    """Internal user profile resource models."""

    first_name = fields.CharField(attribute='user__first_name', null=True)
    last_name = fields.CharField(attribute='user__last_name', null=True)

    class Meta(object):
        """Internal user profile resource meta data."""

        queryset = UserProfile.objects.all().prefetch_related('user') # noqa
        fields = ['id']
        resource_name = 'auth/user'
        authentication = ApiKeyAuthenticationExt()
        authorization = Authorization()
        filtering = {
            "id": 'exact'
        }


class UserProfileResource(MultipartResource, ModelResource):
    """User profile resource models."""

    user = fields.ToOneField(InternalUserResource, attribute='user', null=True)
    first_name = fields.CharField(attribute='user__first_name', null=True)
    last_name = fields.CharField(attribute='user__last_name', null=True)
    email = fields.CharField(attribute='user__email', null=True)

    class Meta(object):
        """Meta data."""

        queryset = UserProfile.objects.prefetch_related('user')
        resource_name = 'userprofile'
        include_resource_uri = False
        always_return_data = True
        authentication = AccessTokenAuthentication()
        authorization = Authorization()
        validation = UserProfileValidation()

    def hydrate(self, bundle):
        """Tastypie hydrate method."""
        userprofile = User.objects.filter(id=bundle.request.user.id).first() # noqa
        bundle.data['user'] = {
            'id': bundle.request.user.id,
            'first_name': userprofile.first_name,
            'last_name': userprofile.last_name,
            'email': userprofile.email,
        }

        return super(UserProfileResource, self).hydrate(bundle)

    def dehydrate(self, bundle):
        """Tastypie dehydrate method."""
        bundle.data['province_id'] = None
        bundle.data['district_id'] = None
        bundle.data['ward_id'] = None
        province = bundle.obj.contact_province
        district = bundle.obj.contact_district
        ward = bundle.obj.contact_ward
        if province:
            bundle.data['province_id'] = province.id
        if district:
            bundle.data['district_id'] = district.id
        if ward:
            bundle.data['ward_id'] = ward.id
        return bundle

    def prepend_urls(self):
        """Api urls."""
        return [
            url(r"^(?P<resource_name>%s)/send_reset_password%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('send_reset_password'), name="api_send_reset_password"),
            url(r"^(?P<resource_name>%s)/reset_password%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('reset_password'), name="api_reset_password"),
            url(r"^(?P<resource_name>%s)/update_userprofile%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('update_userprofile'), name="api_update_userprofile"),
            url(r"^(?P<resource_name>%s)/get_userprofile%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_userprofile'), name="api_get_userprofile"),
            url(r"^(?P<resource_name>%s)/update_shipping_address%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('update_shipping_address'), name="api_update_shipping_address"),
            url(r"^(?P<resource_name>%s)/get_shipping_address%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_shipping_address'), name="api_get_shipping_address"),
        ]

    def reset_password(self, request, **kwargs):
        """Reset password based on token and new password."""
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))
        token = data.get('token', None)
        retype_new_password = data.get('retype_new_password', None)
        new_password = data.get('new_password', None)
        if token:
            # get email_verification by token
            try:
                email_verification = EmailVerification.objects.get(token=token)
                user = email_verification.user
                # if email_verification is expired do nothing, raise exception
                if email_verification.is_expired is not True:
                    email_verification_resource = EmailVerificationResource()
                    if email_verification_resource.is_expired(token) is not True:
                        # if email_verification is not expired, get all email verification that has
                        # user field (email_verification.user)
                        # and set them expired
                        if new_password is not None:
                            if retype_new_password == new_password:
                                user.set_password(new_password)
                                user.save()
                                list_user_email_verification = []
                                list_user_email_verification = EmailVerification.objects.filter(user=user)
                                for user_email_verification in list_user_email_verification:
                                    user_email_verification.is_expired = True
                                    user_email_verification.save()
                                email_verification.is_expired = True
                                email_verification.date_used = timezone.now()
                                email_verification.save()
                                return self.create_response(request, {'success': True})
                            else:
                                raise CustomBadRequest(
                                    error_type='UNAUTHORIZED',
                                    error_message='New passwords are not the same')
                            return self.create_response(request, {'success': True})
                        else:
                            raise CustomBadRequest(
                                error_type='UNAUTHORIZED',
                                error_message='New passwords must be not None')
                            return self.create_response(request, {'success': False})
                    else:
                        email_verification.is_expired = True
                        email_verification.save()
                        raise CustomBadRequest(
                            error_type='UNAUTHORIZED',
                            error_message='Your Email verification is expired')
                else:
                    raise CustomBadRequest(
                        error_type='UNAUTHORIZED',
                        error_message='Your Email verification is expired')
            except EmailVerification.DoesNotExist:
                raise CustomBadRequest(error_type='UNAUTHORIZED', error_message='Email verification does not exist')
        else:
            raise CustomBadRequest(error_type='UNAUTHORIZED', error_message='Token does not exist')

    def send_reset_password(self, request, **kwargs):
        """Send an email containing information (an token) to reset user's password."""
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))
        # get email input
        email = data.get('email', None)

        try:
            # get user by email
            user = User.objects.get(email=email)
            # create an token based on user
            email_verification_resource = EmailVerificationResource()
            email_verification = email_verification_resource.create_email_verification(request, user)
            token = email_verification.token
            # send an email with above token to user's email
            send_email_reset_password(user, token, "Reset Password", "")
            return self.create_response(request, {'success': True})
        except User.DoesNotExist:
            raise CustomBadRequest(error_type='UNAUTHORIZED', error_message='Your email does not exist')

    def update_userprofile(self, request, **kwargs):
        """Update userprofile informations."""
        self.method_check(request, allowed=['post'])
        self._meta.authentication.is_authenticated(request)
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))

        # get usre
        user = request.user
        try:
            # get userprofile by user
            userprofile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise CustomBadRequest(error_type='UNAUTHORIZED', error_message='User Profile does not exist!')
        # Browse every key in data, update any field that has value
        # If field is email -> send an email to verify email
        # if field is name -> update email in both model User and UserProfile
        for key, value in data.items():
            if key == 'email':
                pass
                # setattr(userprofile, key, value)
                # setattr(user, key, value)
                # email_verification = email_verification_resource.create_email_verification(request, user)
                # token = email_verification.token
                # send_email(user, token, "Registration", "Hello!")
            elif key == 'first_name' or key == 'last_name':
                setattr(userprofile, key, value)
                setattr(user, key, value)
                user.save()
            elif key == 'contact_province_id':
                setattr(userprofile, 'contact_province', Province.objects.get(pk=value))
            elif key == 'contact_district_id':
                setattr(userprofile, 'contact_district', District.objects.get(pk=value))
            elif key == 'contact_ward_id':
                setattr(userprofile, 'contact_ward', Ward.objects.get(pk=value))
            else:
                setattr(userprofile, key, value)
            setattr(userprofile, 'date_last_update', timezone.now())
        # Save information
        user.save()
        userprofile.save()
        return self.create_response(request, {'updated': True})

    def get_userprofile(self, request, **kwargs):
        """Update userprofile informations."""
        self.method_check(request, allowed=['get'])
        self._meta.authentication.is_authenticated(request)

        # get usre
        user = request.user
        try:
            # get userprofile by user
            userprofile = UserProfile.objects.get(user=user)
            bundle = self.build_bundle(request=request, obj=userprofile)
            bundle = self.full_dehydrate(bundle)
            return self.create_response(request, bundle)
        except UserProfile.DoesNotExist:
            raise CustomBadRequest(error_type='UNAUTHORIZED', error_message='User Profile does not exist!')

    def update_shipping_address(self, request, **kwargs):
        """Create or update user's address."""
        self.method_check(request, allowed=['post'])
        self._meta.authentication.is_authenticated(request)
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))
        user = request.user
        address_resource = AddressResource()
        address_resource.create_or_update_address(data=data, user=user)
        return self.create_response(request, {'Success': True})

    def get_shipping_address(self, request, **kwargs):
        """Get shipping address of this user."""
        self.method_check(request, allowed=['get'])
        self._meta.authentication.is_authenticated(request)

        try:
            address = Address.objects.get(user=request.user)
            address_resource = AddressResource()
            bundle = address_resource.build_bundle(request=request, obj=address)
            bundle = address_resource.full_dehydrate(bundle)
            return self.create_response(request, bundle)
        except Address.DoesNotExist:
            raise CustomBadRequest(error_type='INVALID_DATA',
                                   error_message='This user does not input shipping address!')


class AuthenticationResource(ModelResource):
    """Authentication resource."""

    class Meta(object):
        """Meta data."""

        allowed_methods = ['get', 'post']
        always_return_data = True
        authentication = AccessTokenAuthentication()
        authorization = Authorization()
        queryset = User.objects.all() # noqa
        resource_name = 'authentication'
        fields = ['username', 'email', 'password', 'image']

    def prepend_urls(self):
        """Api urls."""
        return [
            url(r"^(?P<resource_name>%s)/sign_in%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('sign_in'), name="api_sign_in"),
            url(r"^(?P<resource_name>%s)/sign_up%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('sign_up_by_email'), name="api_sign_up_by_email"),
            url(r"^(?P<resource_name>%s)/sign_out%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('sign_out'), name="api_sign_out"),
            url(r"^(?P<resource_name>%s)/change_password%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('change_password'), name="api_change_password"),
            url(r"^(?P<resource_name>%s)/getuserinfo%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_user_info'), name="api_get_user_info"),
            url(r"^(?P<resource_name>%s)/update_address%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('update_address'), name="api_update_address"),
            url(r"^(?P<resource_name>%s)/loginsocial%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login_social'), name="api_login_social"),
            url(r"^(?P<resource_name>%s)/verify_email%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('verify_email'), name="api_verify_email"),
        ]

    def verify_email(self, request, **kwargs):
        """Verify email based on email verification."""
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))
        token = data.get('token', None)
        if token:
            # get email_verification by token
            try:
                email_verification = EmailVerification.objects.get(token=token)
                user = email_verification.user
                # if email_verification is expired do nothing, raise exception
                if email_verification.is_expired is not True:
                    email_verification_resource = EmailVerificationResource()
                    if email_verification_resource.is_expired(token) is not True:
                        # if email_verification is not expired, get all email verification that has
                        # user field (email_verification.user)
                        # and set them expired
                        list_user_email_verification = []
                        list_user_email_verification = EmailVerification.objects.filter(user=user)
                        for user_email_verification in list_user_email_verification:
                            user_email_verification.is_expired = True
                            user_email_verification.save()
                        email_verification.date_used = timezone.now()
                        email_verification.is_expired = True
                        email_verification.save()
                        user.is_active = True
                        user.save()
                        return self.create_response(request, {'is_acitve': user.is_active})
                    else:
                        email_verification.is_expired = True
                        email_verification.save()
                        raise CustomBadRequest(
                            error_type='UNAUTHORIZED',
                            error_message='Your Email verification is expired')
                else:
                    raise CustomBadRequest(
                        error_type='UNAUTHORIZED',
                        error_message='Your Email verification is expired')
            except EmailVerification.DoesNotExist:
                raise CustomBadRequest(error_type='UNAUTHORIZED', error_message='Email verification does not exist')
        else:
            raise CustomBadRequest(error_type='UNAUTHORIZED', error_message='Token does not exist')

    def change_password(self, request, **kwargs):
        """Method to control password changing."""
        self.method_check(request, allowed=['post'])
        self._meta.authentication.is_authenticated(request)
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))
        # get information on params
        old_password = data.get('old_password', None)
        new_password = data.get('new_password', None)
        retype_new_password = data.get('retype_new_password', None)
        # get user and check authentication
        user = request.user
        if user.check_password(old_password):
            user = authenticate(username=user.email, password=old_password)
            if new_password is not None:
                if retype_new_password == new_password:
                    # set new password
                    user.set_password(new_password)
                    user.save()
                    return self.create_response(request, {'success': True})
                else:
                    raise CustomBadRequest(
                        error_type='UNAUTHORIZED',
                        error_message='New passwords are not the same')
            else:
                raise CustomBadRequest(error_type='UNAUTHORIZED', error_message='Password must be not None')

        else:
            raise CustomBadRequest(error_type='UNAUTHORIZED', error_message='Your password is not correct')

    def sign_in(self, request, **kwargs):
        """Sign in api handler."""
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))
        retype_password = data.get('retype_password', None)
        if retype_password is not None:
            return self.sign_up_by_email(request, **kwargs)
        elif 'email' in data and 'password' in data:
            return self.sign_in_by_email(request, **kwargs)
        else:
            raise CustomBadRequest(error_type='UNAUTHORIZED')

    def sign_in_by_email(self, request, **kwargs):
        """Sign in by email api handler."""
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))
        email = data.get('email', '')
        password = data.get('password', '')
        try:
            user = User.objects.get(email=email) # noqa
            if user.check_password(password):
                if user.is_active:
                    user = authenticate(username=email, password=password)
                    login(request, user)
                    accesstoken_resource = AccessTokenResource()
                    access_token = accesstoken_resource.create_accesstoken(request, user, data)
                    apikey = ApiKey.objects.filter(user=user).first()
                    return self.create_auth_response(
                        request=request,
                        user=user,
                        api_key=apikey.key,
                        access_token=access_token)
                else:
                    raise CustomBadRequest(error_type='UNAUTHORIZED', error_message='Your email is not verified')
        #         else:
        #             return self.create_response(request=request, data='email sai')
            else:
                raise CustomBadRequest(error_type='UNAUTHORIZED', error_message='Your password is not correct')
        #     else:
        #         return self.create_response(request=request, data='password sai')
        except User.DoesNotExist:
            raise CustomBadRequest(error_type='UNAUTHORIZED',
                                   error_message='Your email address is not registered. Please register')
        #     return self.create_response(request=request, data='email chua dang ky')

    def sign_up_by_email(self, request, **kwargs):
        """Sign up by email handler."""
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))
        # data = request.POST
        return self.create_user(request, data)

    def create_user(self, request, data, is_active=False):
        """Provice helper funtion for create user."""
        email = data.get('email', '')
        password = data.get('password', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        image = data.get('image', '')
    #
        if last_name:
            last_name = last_name.strip()
        if first_name:
            first_name = first_name.strip()

        # Check email exist in system.
        if User.objects.filter(email__iexact=email).exists(): # noqa
            raise CustomBadRequest(error_type='DUPLICATE_VALUE', field='email', obj='email')
        else:
            try:
                with transaction.atomic():
                    # If create user with social network!
                    if is_active and password == '':
                        import random
                        # Random password to be sure user cant login with this user
                        password = password.join(
                            random.choice(
                                "akshf@23#@@323ajsf233@#@#2343$@*$ASSad2123@#@223123#asdKWADJ*#*&@") for _ in range(10))
                    # Create user with paramaters
                    User.objects.create_user(
                        username=email, email=email, password=password, first_name=first_name, last_name=last_name, is_active=is_active) # noqa
                    user = authenticate(username=email, password=password)

                    login(request, user)

                    if user is not None:
                        # Create user profile
                        self.create_userprofile(user.id)
                        apikey = ApiKey.objects.filter(user=user).first()
                        access_token = None
                        # If create account with normal register => send active email.
                        if not is_active:
                            send_email(user, "", "Registration", "Hello!")
                        # If create account with social => create a access_token for user
                        else:
                            accesstoken_resource = AccessTokenResource()
                            access_token = accesstoken_resource.create_accesstoken(request, user, data)
                        UserProfile.objects.filter(user__id=user.id).update(
                            image=image,
                            first_name=first_name,
                            last_name=last_name)

                        # update social info
                        self.add_social_info(user=user, data=data)
                        if access_token is not None:
                            return self.create_auth_response(
                                request=request,
                                user=user,
                                api_key=apikey.key,
                                access_token=access_token)
                        else:
                            return self.create_auth_response(
                                request=request,
                                user=user,
                                api_key=apikey.key)
                    else:
                        raise CustomBadRequest(error_type='UNKNOWN_ERROR', error_message='Cant sign up by this email.')
            except ValueError as e:
                raise CustomBadRequest(error_type='UNKNOWN_ERROR', error_message=str(e))

    def sign_out(self, request, **kwargs):
        """Sign out handler."""
        self._meta.authentication.is_authenticated(request)
        self.method_check(request, allowed=['post', 'get'])
        access_token = self._meta.authentication.extract_credentials(request)
        print(request.META.get('HTTP_AUTHORIZATION', ''))
        print("access_token" + access_token)
        user = self.logout(request, access_token)
        request.user = user
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)

    def create_auth_response(self, request, user, api_key, access_token=None):
        """Genetate response data for authentication process."""
        userprofile = UserProfile.objects.get(id=user.userprofile.id) # noqa

        resource_instance = UserProfileResource()
        bundle = resource_instance.full_hydrate(resource_instance.build_bundle(obj=userprofile, request=request))
        bundle.data['user']['api_key'] = api_key

        if access_token:
            bundle.data['user']['access_token'] = access_token.access_token
        return self.create_response(request, bundle)

    def create_userprofile(self, user_id, **kwargs):
        """Create blank user profile base on user_id."""
        # Add the user_id to kwargs
        kwargs['user_id'] = user_id

        # register_type = kwargs.get('register_type', None)
        # is_facebook = register_type == 1

        # Create user profile
        userprofile, _ = UserProfile.objects.get_or_create(user__id=user_id, defaults=kwargs) # noqa

        if userprofile is None:
            raise CustomBadRequest(error_type='UNKNOWNERROR', error_message="Can't create userprofile and address")

    def get_user_info(self, request, **kwargs):
        """Provide api to get normal user info."""
        self.method_check(request, allowed=['get'])
        self._meta.authentication.is_authenticated(request)

        user = request.user
        bundle = self.build_bundle(request)
        bundle.data['user'] = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        # try:
        #     bundle.data['user']['is_seller'] = False
        #     Seller.objects.get(user=user)
        #     bundle.data['user']['is_seller'] = True
        # except Seller.DoesNotExist:
        #     pass
        return self.create_response(request, bundle)

    def logout(self, request, access_token, **kwargs):
        """Support api to get user."""
        if access_token is not None:
            # get user with access token
            access_token_resource = AccessTokenResource()
            user = access_token_resource.get_user(access_token)
            access_token_resource.set_expired(access_token)
            return user
        else:
            raise CustomBadRequest(error_type='UNLOGIN', error_message='Please add access token to request paramater')

    def login_social(self, request, **kwargs):
        """Provice api for login by facebook."""
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/join'))
        linked_user_id = data.get('linked_user_id', None)
        try:
            # Check this social account exist in system.
            user_login_account = UserLoginAccount.objects.get(linked_user_id=linked_user_id)
            user = user_login_account.user
            request.user = user
            print("user: ", user)
            # update user info
            self.add_social_info(user=user, data=data)
            # update some info of user
            accesstoken_resource = AccessTokenResource()
            access_token = accesstoken_resource.create_accesstoken(request, user, data)
            apikey = ApiKey.objects.filter(user=user).first()
            return self.create_auth_response(
                request=request,
                user=user,
                api_key=apikey.key,
                access_token=access_token)
        except UserLoginAccount.DoesNotExist:
            # Check user email exist in system.
            email = data.get('email', None)
            print("email: ", email)
            try:
                user = User.objects.get(email=email)
                raise CustomBadRequest(error_type='ACCOUNT_EXIST')
            except User.DoesNotExist:
                # create new user
                return self.create_user(request, data, True)
        except UserLoginAccount.MultipleObjectsReturned:
            raise CustomBadRequest(error_type='INVALID_DATA', error_message='Have multiple social info!')

    def add_social_info(self, user, data):
        """Helper function for add social info."""
        account_id = data.get('account_id', None)
        if account_id is not None:
            account_key = data.get('account_key', None)
            account_secret = data.get('account_secret', None)
            request_permission = data.get('request_permission', '')
            login_type = data.get('login_type', None)
            updated_values = {
                'account_key': account_key,
                'account_secret': account_secret,
                'request_permission': request_permission,
                'name': login_type
            }
            login_account_type, created = LoginAccountType.objects.update_or_create(
                account_id=account_id,
                defaults=updated_values)
            linked_user_id = data.get('linked_user_id', None)
            access_token = data.get('access_token', None)
            granted_permissions = data.get('granted_permissions', None)
            updated_values = {
                'linked_user_id': linked_user_id,
                'access_token': access_token,
                'granted_permissions': granted_permissions
            }
            UserLoginAccount.objects.update_or_create(
                user=user,
                login_account_type=login_account_type,
                defaults=updated_values)


class AccessTokenResource(ModelResource):
    """This class provide api for access to access token."""

    class Meta(object):
        """Meta data."""

        queryset = AccessToken.objects.all()
        resource_name = 'accesstoken'
        always_return_data = True
        authentication = ApiKeyAuthenticationExt()
        authorization = NoAccessAuthorization()

    def create_accesstoken(self, request, user, data):
        """Create a access token after user login to system."""
        device_type = data.get('device_type', 'WEB')
        language_code = data.get('language_code', 'EN')
        phone_token = data.get('phone_token', '')
        phone_type = data.get('phone_type', '')
        return AccessToken.objects.create(
            device_type=device_type,
            user=user,
            language_code=language_code,
            phone_token=phone_token,
            phone_type=phone_type)

    def is_expired(self, access_token):
        """Check access token is expired or not."""
        try:
            token = AccessToken.objects.get(access_token=access_token)
            if token.is_expired:
                return True
            access_time = token.access_time
            now_time = timezone.now()
            delta = now_time - access_time
            token.save()
            if delta.seconds / 60 > 30:
                return True
            else:
                return False
        except AccessToken.DoesNotExist:
            raise CustomBadRequest(error_type='INVALID_DATA', error_message='Access token is not valid.')
        except ValueError:
            raise CustomBadRequest(error_type='INVALID_DATA', error_message='Access token is not valid.')

    def set_expired(self, access_token, is_expired=True):
        """Set access_token to expired when user logout."""
        try:
            token = AccessToken.objects.get(access_token=access_token)
            token.is_expired = is_expired
            token.save()
        except AccessToken.DoesNotExist:
            raise CustomBadRequest(error_type='INVALID_DATA', error_message='Access token is not valid.')

    def get_user(self, access_token):
        """Provide api to get user have access token in DB."""
        if not self.is_expired(access_token):
            try:
                user = User.objects.get(accesstoken__access_token=access_token)
                return user
            except User.DoesNotExist:
                raise CustomBadRequest(error_type='INVALID_DATA', error_message='Can get user with access token')
        else:
            raise CustomBadRequest(error_type='UNLOGIN', error_message='Access token expired')


class AddressValidation(Validation):
    """Docstring for AddressValidation."""

    def is_valid(self, bundle, request=None):
        """Helper function to check bundle data valid or not valid."""
        if not bundle:
            return {'__all__': 'Input data not found!'}

        errors = {}
        if 'full_name' not in bundle:
            errors["full_name"] = ['You must enter full_name.']
        if 'address' not in bundle:
            errors["address"] = ['You must enter address.']
        if 'phone_number' not in bundle:
            errors["phone_number"] = ['You must enter phone_number.']
        if 'province_id' not in bundle:
            errors["province_id"] = ['You must enter province_id.']
        if 'district_id' not in bundle:
            errors["district_id"] = ['You must enter district_id.']
        if 'ward_id' not in bundle:
            errors["ward_id"] = ['You must enter ward_id.']
        return errors
