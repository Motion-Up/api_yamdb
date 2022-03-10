from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title
from users.models import CustomUser
from .permissions import (
    IsAdminOrReadOnly,
    AuthorAdminModeratorOrReadOnly,
    IsAuthorOnlyPermission,
    AuthorOrReadOnly,
    IsAdminPermission
)
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    RegisterSerializer, ReviewSerializer, TitleCreateSerializer,
    TitleSerializer, UserSerializer, TokenSerializer, OwnerSerializer
)
from .filters import TitleFilter


class CreateListDestroyMixin(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateListDestroyMixin):
    queryset = Category.objects.all().order_by('-id')
    pagination_class = PageNumberPagination
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyMixin):
    queryset = Genre.objects.all().order_by('-id')
    pagination_class = PageNumberPagination
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(Avg('reviews__score')).order_by('-id')
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AuthorAdminModeratorOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorAdminModeratorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serializer = RegisterSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid(raise_exception=True):
        if serializer.data['username'] == 'me':
            raise serializers.ValidationError(
                "Нельзя называть пользователя me"
            )
        user = CustomUser.objects.create(
            username=serializer.data['username'],
            email=serializer.data['email'],
            password=serializer.data['email']
        )
        user.save()
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Register code',
            f'{confirmation_code}',
            'admin@yandex.ru',
            [serializer.data['email']],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(
            CustomUser,
            username=serializer.data['username']
        )
        if default_token_generator.check_token(
            user,
            request.data['confirmation_code']
        ):
            token = AccessToken.for_user(user)
            return Response(
                {'token': f'{token}'},
                status=status.HTTP_200_OK
            )

    return Response(
        {'message': 'Пользователь не обнаружен'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = (IsAdminPermission,)
    lookup_field = 'username'


class OwnerUserView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = OwnerSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthorOnlyPermission,)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)
        return obj
