from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (SignUpCreate, UserProfileViewSet,
                    get_jwt_token, CommentViewSet, ReviewViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('users', UserProfileViewSet, basename='profile')
router.register('auth/signup', SignUpCreate, basename='signup')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/auth/token/', get_jwt_token, name='token'),
    path('v1/', include(router.urls)),
]
