from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from users.utils import validate_serializer


class UserSerializer(serializers.ModelSerializer):
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

    def validate(self, data):
        """Валидация полей."""
        return validate_serializer(data)


class CreationUserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели `User` для создания пользователя."""

    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, username):
        """Валидация поля `username`."""
        if username == "me":
            raise serializers.ValidationError('Имя `me` нельзя использовать!')
        return username

    def validate(self, data):
        """Валидация полей"""
        return validate_serializer(data)


class TokenSerializer(TokenObtainSerializer):
    """Сериализатор для выдачи токена."""

    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["confirmation_code"] = serializers.CharField(required=True)
        self.fields["password"] = serializers.HiddenField(default="")

    def validate(self, data):
        """Валидвция данных."""
        user = get_object_or_404(User, username=data["username"])
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
