from django.urls import include, path

from .views import CommentViewSet, ReviewViewSet

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='title_id'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='review_id'


urlpatterns = [
    path('v1/', include(router.urls)),
]