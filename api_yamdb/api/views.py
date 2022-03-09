import random
import string

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as django_filters
from django.core.mail import send_mail
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers

from reviews.models import Category, Genre, Review, Title
from users.models import CustomUser
from .permissions import (
    IsAdminPermission,
    IsAuthorOnlyPermission,
    AuthorOrReadOnly
)
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    RegisterSerializer, ReviewSerializer, TitleCreateSerializer,
    TitleSerializer, TokenSerializer, UserSerializer
)


class CreateListDestroyMixin(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateListDestroyMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes =
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    filter_backends = (django_filters.DjangoFilterBackend,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        letters_and_digits = string.ascii_letters + string.digits
        rand_string = ''.join(random.sample(letters_and_digits, 8))
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data['username'] == 'me':
                raise serializers.ValidationError(
                    "Нельзя называть пользователя me"
                )
            user = CustomUser.objects.create(
                username=serializer.data['username'],
                email=serializer.data['email'],
                password=rand_string,
                confirmation_code=rand_string
            )
            user.save()
            send_mail(
                'Register code',
                f'{rand_string}',
                'admin@yandex.ru',
                [serializer.data['email']],
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        {'message': 'Пользователь не обнаружен'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminPermission,)


class OwnerUserView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthorOnlyPermission,)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)
        return obj
