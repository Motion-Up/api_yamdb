from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .permission import AuthorOrReadOnly
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleCreateSerializer,
                          TitleSerializer)
from rest_framework import mixins, viewsets

from reviews.models import Title, Genre, Title


class CreateListDestroyMixin(mixins.CreateModelMixin, mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDestroyMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes =
    filter_backends = (SearchFilter, )
    search_fields = ('name', )


class GenreViewSet(CreateListDestroyMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name', )


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(Avg('reviews__rating'))
    filter_backends = (DjangoFilterBackend, )
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer