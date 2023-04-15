from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import IntegerField
from rest_framework.relations import SlugRelatedField

from reviews.models import Title, Genre, Category, Review, Comment


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для действий по жанрам."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для действий по категориям."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'year',
                  'rating', 'genre', 'category')
        read_only_fields = ('rating',)


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления произведений."""
    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all(),
                                many=False)
    genre = SlugRelatedField(slug_field='slug',
                             queryset=Genre.objects.all(),
                             many=True)

    class Meta:
        fields = ('id', 'name', 'description',
                  'rating', 'year', 'genre', 'category')
        model = Title
        read_only_fields = ('rating',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    title = SlugRelatedField(slug_field='name',
                             read_only=True)

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
                request.method == 'POST'
                and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Вы можете оставить только '
                                  '1 отзыв на одно и то же произведение!')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    review = SlugRelatedField(slug_field='text',
                              read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
