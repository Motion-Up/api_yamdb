from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    # App User
    path('auth/signup/', views.RegisterView.as_view(), name='register'),
    path('auth/token/', views.create_token, name='token'),
]