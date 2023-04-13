from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAdmin
from users.models import User
from users.serializers import (
    CreationUserSerializer,
    ProfileSerializer,
    UserSerializer,
)
from users.utils import send_code


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


@api_view(["GET", "PATCH"])
@permission_classes(
    [
        IsAuthenticated,
    ],
)
def get_me(request):
    """Сериализатор профиля пользователя."""
    if request.method == "PATCH":
        serializer = ProfileSerializer(
            request.user, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    serializer = ProfileSerializer(request.user)
    return Response(serializer.data)


class SignUpAPIView(generics.CreateAPIView):
    """Вью-функция для создания пользователя."""

    serializer_class = CreationUserSerializer

    def post(self, request):
        """Cохранение нового/существующего экземпляра объекта."""
        if User.objects.filter(username=request.data.get('username')).exists():
            user = User.objects.get(username=request.data.get('username'))
            serializer = self.serializer_class(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            send_code(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_code(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
