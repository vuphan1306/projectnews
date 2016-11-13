# -*- coding: utf-8 -*-
"""urls."""
from __future__ import absolute_import
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from tastypie.api import Api
# from django.views.generic import TemplateView
from django.views import defaults as default_views
from backend.article.api import ArticleResource
# from backend.task.api import TaskResource
from backend.account.api import AuthenticationResource, UserProfileResource, UserResource
# from backend.order.api import OrderProductResource, OrderResource
# from backend.ideabook.api import IdeaBookResource, IdeaBookUserResource
# from backend.image.api import FileResource, ProductFileRelationshipResource
# from backend.product.api import ProductResource, CategoryQueryResource, StyleQueryResource
# from backend.internationalization.api import LanguageResource
# from backend.message.api import MessageResource
# from backend.review.api import ReviewResource, ReviewRequestResource
# from backend.project.api import ProjectResource
# from backend.question.api import QuestionResource, QuestionProductResource
from backend.comment.api import CommentResource
# from backend.sale.api import DiscountCampaignResource
# from backend.address.api import ProvinceResource, DistrictResource, WardResource
# from backend.dataloader.api import DataLoader
from backend.category.api import CategoryResource
v1_api = Api(api_name='v1')
v1_api.register(UserProfileResource())
v1_api.register(AuthenticationResource())
v1_api.register(UserResource())
# v1_api.register(SellerResource())
# v1_api.register(TaskResource())
# v1_api.register(OrderProductResource())
# v1_api.register(OrderResource())
# v1_api.register(ProductResource())
v1_api.register(CategoryResource())
# v1_api.register(StyleQueryResource())
# v1_api.register(LanguageResource())
# v1_api.register(MessageResource())
# v1_api.register(ReviewResource())
# v1_api.register(ReviewRequestResource())
# v1_api.register(IdeaBookResource())
# v1_api.register(IdeaBookUserResource())
# v1_api.register(FileResource())
# v1_api.register(ProductFileRelationshipResource())
# v1_api.register(ProjectResource())
# v1_api.register(QuestionResource())
# v1_api.register(QuestionProductResource())
v1_api.register(CommentResource())
# v1_api.register(DiscountCampaignResource())
# v1_api.register(ProvinceResource())
# v1_api.register(DistrictResource())
# v1_api.register(WardResource())
# v1_api.register(DataLoader())
v1_api.register(ArticleResource())

urlpatterns = [

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),
    url(
        r'api/v1/docs/',
        include('tastypie_swagger.urls', namespace='v1_tastypie_swagger'),
        kwargs={"tastypie_api_module": "config.urls.v1_api", "namespace": "v1_tastypie_swagger"}),
    # User management
    url(r'^api/', include(v1_api.urls)),
    # url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    import debug_toolbar
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception("Bad Request!")}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception("Permissin Denied")}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
        url(r'^500/$', default_views.server_error),
        url(r'^__debug__', include(debug_toolbar.urls)),
    ]
