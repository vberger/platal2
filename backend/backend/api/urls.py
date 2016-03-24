from django.conf.urls import include, url
from rest_framework import routers

from .resources import account
from .resources import profile


router = routers.DefaultRouter()
router.register(r'accounts', account.AccountViewSet, base_name='accounts')
router.register(r'profiles', profile.ProfileViewSet)
router.register(r'photos', profile.ProfilePhotoViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'photos/(?P<hrpid>.+)/raw/', profile.RawPhotoView.as_view(), name='profile-photo-raw'),
]
