from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from users.models import CustomUser
from .serializers import RegisterSerializer, TokenSerializer, UserSerializer
from .permissions import IsAdminPermission


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def create_token(request):
    user = get_object_or_404(
        CustomUser,
        username=request.data['username']
    )
    serializer = TokenSerializer(data=request.data)
    if user.confirmation_code == request.data['confirmation_code']:
        token = serializer.get_token(user)
        return Response(
            token,
            status=status.HTTP_200_OK
        )

    return Response(
        {'data': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminPermission,)
