import uuid

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAdmin
from users.models import User
from users.serializers import (
    CreationUserSerializer,
    ProfileSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели `User`."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAdmin,
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_serializer_class(self):
        if self.action == "me":
            return ProfileSerializer
        return self.serializer_class

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request, pk=None):
        """Сериализатор профиля пользователя."""
        if request.method == "PATCH":
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class SignUpAPIView(generics.CreateAPIView):
    """Вью-функция для создания пользователя."""

    serializer_class = CreationUserSerializer

    def post(self, request):
        """Cохранение нового/существующего экземпляра объекта."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
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
        return Response(serializer.data, status=status.HTTP_200_OK)
