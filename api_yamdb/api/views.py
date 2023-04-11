from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitleFilter

from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from .serialazers import TitleReadSerializer, TitleWriteSerializer, CategorySerializer, GenreSerializer
from api_yamdb.reviews.models import Title, Genre, Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes =
    filter_backends = (SearchFilter,)
    search_fields = ('slug',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes =
    filter_backends = (SearchFilter,)
    search_fields = ('slug',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = GenreSerializer
    # permission_classes =
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update',):
            return TitleWriteSerializer
        return TitleReadSerializer
