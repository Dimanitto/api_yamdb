from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   views.ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', views.CommentViewSet, basename='comments')
router = SimpleRouter()
router.register(r'titles', views.TitleViewSet, basename='titles')
router.register(r'genres', views.GenreViewSet, basename='genres')
router.register(r'categories', views.CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router_v1.urls, router.urls)),
]
