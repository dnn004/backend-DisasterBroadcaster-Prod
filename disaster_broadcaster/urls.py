from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

from disaster_broadcaster.views.Authenticate import AuthenticateUser, LogoutUser, PasswordReset
from disaster_broadcaster.views.User import UserViewset
from disaster_broadcaster.views.Reaction import ReactionViewset
from disaster_broadcaster.views.Post import PostViewset
from disaster_broadcaster.views.Organization import OrganizationViewset
from disaster_broadcaster.views.News import NewsViewset
from disaster_broadcaster.views.Fund import FundViewset
from disaster_broadcaster.views.Disaster import DisasterViewset
from disaster_broadcaster.views.Country import CountryViewset
from disaster_broadcaster.views.Comment import CommentViewset
from disaster_broadcaster.views.Category import CategoryViewset


router = routers.DefaultRouter()
router.register('user', UserViewset, basename='user')
router.register('reaction', ReactionViewset, basename='raction')
router.register('post', PostViewset, basename='post')
router.register('organization', OrganizationViewset, basename='organization')
router.register('news', NewsViewset, basename='news')
router.register('fund', FundViewset, basename='fund')
router.register('disaster', DisasterViewset, basename='disaster')
router.register('country', CountryViewset, basename='country')
router.register('comment', CommentViewset, basename='comment')
router.register('category', CategoryViewset, basename='category')

urlpatterns = [
  url(r'^', include(router.urls)),
  url(r'^user-authenticate/', AuthenticateUser),
  url(r'^logout/', LogoutUser),
  url(r'^password-reset/', PasswordReset)
]

