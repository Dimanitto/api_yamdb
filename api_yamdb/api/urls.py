from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SignUpCreate, GetToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = 'api'

router = DefaultRouter()
#router.register('auth/signup', SignUpCreate.as_view(), basename='signup')


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/', GetToken.as_view(), name='token'),
    path('auth/signup/', SignUpCreate.as_view(), name='signup'),
    #path('', include(router.urls)),
]
