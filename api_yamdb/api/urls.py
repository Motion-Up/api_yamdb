from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()


router.register(
    'categories',
    views.CategoryViewSet,
    basename='сategory'
)
router.register(
    'titles',
    views.TitleViewSet,
    basename='title'
)
router.register(
    'genres',
    views.GenreViewSet,
    basename='genre'
)
router.register(
    'users',
    views.UserView
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='title_id'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='review_id'
)

urlpatterns = [
    path('auth/signup/', views.RegisterView.as_view(), name='register'),
    path('auth/token/', views.create_token, name='token'),
    path('users/me/', views.OwnerUserView.as_view(), name='owner'),
    path('', include(router.urls)),
    path('v1/', include(router.urls)),
]
