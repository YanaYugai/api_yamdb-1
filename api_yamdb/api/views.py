from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitleFilter

from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from .serialazers import TitleReadSerializer, TitleWriteSerializer, CategorySerializer, GenreSerializer, ReviewSerializer, CommentSerializer
from reviews.models import Title, Genre, Category, Review


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes =
    filter_backends = (SearchFilter,)
    search_fields = ('slug',)


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes =
    filter_backends = (SearchFilter,)
    search_fields = ('slug',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""
    queryset = Title.objects.all()
    serializer_class = GenreSerializer
    # permission_classes =
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update',):
            return TitleWriteSerializer
        return TitleReadSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes =

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()
    
    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes =

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)

