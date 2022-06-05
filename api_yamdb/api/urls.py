from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUpCreate, UserProfileViewSet, get_jwt_token

app_name = 'api'

router = DefaultRouter()
router.register('users', UserProfileViewSet, basename='profile')
router.register('auth/signup', SignUpCreate, basename='signup')


urlpatterns = [
    path('auth/token/', get_jwt_token, name='token'),
    path('', include(router.urls)),
]
