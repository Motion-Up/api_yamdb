from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views
from .views import CommentViewSet, ReviewViewSet

router = SimpleRouter()

router.register('users', views.UserView)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='title_id'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='review_id'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/signup/', views.RegisterView.as_view(), name='register'),
    path('auth/token/', views.create_token, name='token'),
    path('', include(router.urls)),
]
