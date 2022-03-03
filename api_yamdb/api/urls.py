from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet


router = SimpleRouter()

router.register(
    'categories',
    CategoryViewSet,
    basename='сategory'
)
router.register(
    'titles',
    TitleViewSet,
    basename='title'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genre'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]