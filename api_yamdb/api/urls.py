from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   views.ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', views.CommentViewSet, basename='comments')
router = DefaultRouter()
router.register(r'titles', views.TitleViewSet, basename='titles')
router.register(r'genres', views.GenreViewSet, basename='genres')
router.register(r'categories', views.CategoryViewSet, basename='categories')

router.register('users', views.UserProfileViewSet, basename='profile')
router.register('auth/signup', views.SignUpCreate, basename='signup')


urlpatterns = [
    path('v1/auth/token/', views.get_jwt_token, name='token'),
    path('v1/', include(router.urls)),
    path('v1/', include(router_v1.urls)),
]
