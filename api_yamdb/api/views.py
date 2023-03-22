from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin
)
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.filters import TitleFilterSet
from api.serializers import (
    CategoriesSerializer, GenreSerializer,
    GetTitleSerializer, PostTitleSerializer
)
from reviews.models import Categories, Genre, Title
from api.permissions import IsAdminOrReadOnly


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdminOrReadOnly, )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetTitleSerializer
        return PostTitleSerializer


class CategoryGenreDefaultViewSet(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly, )


class GenreViewSet(CategoryGenreDefaultViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoriesViewSet(CategoryGenreDefaultViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
