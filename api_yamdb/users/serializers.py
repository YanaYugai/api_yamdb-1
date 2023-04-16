from django.db.utils import IntegrityError
from django.http import Http404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User


class CreationUserSerializer(serializers.ModelSerializer):
    """Сериализатор с расширенным методом `create`."""

    def create(self, validated_data):
        try:
            user, created = User.objects.get_or_create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                'Используйте другую почту или имя пользователя!',
            )
        return user


class UserSerializer(CreationUserSerializer):
    """Сериализатор для модели `User`."""

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]


class CreationUserSerializer(CreationUserSerializer):
    """Сериализатор для модели `User` для создания пользователя."""

    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, username):
        """Валидация поля `username`."""
        if username == "me":
            raise serializers.ValidationError('Имя `me` нельзя использовать!')
        return username


class TokenSerializer(TokenObtainSerializer):
    """Сериализатор для выдачи токена."""

    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["confirmation_code"] = serializers.CharField(required=True)
        del self.fields["password"]

    def validate(self, data):
        """Валидация данных."""
        try:
            user = User.objects.get(username=data["username"])
        except User.DoesNotExist:
            raise Http404(
                "Не найден пользователь или неправильный код подтверждения!",
            )
        if user.confirmation_code != data["confirmation_code"]:
            raise serializers.ValidationError("Неверный код!")
        return {'token': str(self.get_token(user))}


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор Профиля."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)
