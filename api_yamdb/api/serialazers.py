from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Title, Genre, Category, Review, Comment


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для действий по жанрам."""

    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для действий по категориям."""

    class Meta:
        fields = '__all__'
        model = Category


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления произведений."""
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),

    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Review

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'