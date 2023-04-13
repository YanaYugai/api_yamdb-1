import uuid
from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import serializers

from users.models import User


def validate_serializer(data: Any):
    """Функция для валидации полей сериализаторов."""
    if User.objects.filter(
        email=data.get('email'), username=data.get('username'),
    ).exists():
        return data
    if (
        User.objects.filter(email=data.get('email')).exists()
        or User.objects.filter(username=data.get('username')).exists()
    ):
        raise serializers.ValidationError(
            'Используйте другой useranme или email',
        )
    return data


def send_code(serializer):
    """Функция отправки кода."""
    code = uuid.uuid4()
    user = serializer.save()
    user.confirmation_code = code
    user.save()
    send_mail(
        'Confirmation code',
        f'Your code {code}',
        settings.MY_EMAIL,
        [user.email],
        fail_silently=False,
    )
