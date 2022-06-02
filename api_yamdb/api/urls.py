from django.urls import path, include

from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'titles', views.TitleViewSet, basename='titles')
router.register(r'genres', views.GenreViewSet, basename='genres')
router.register(r'categories', views.CategoryViewSet, basename='categories')


urlpatterns = [
    path('v1/', include(router.urls))
]
