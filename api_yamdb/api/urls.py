from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register('users', views.UserView)

urlpatterns = [
    # App User
    path('auth/signup/', views.RegisterView.as_view(), name='register'),
    path('auth/token/', views.create_token, name='token'),
    path('', include(router.urls)),
]
