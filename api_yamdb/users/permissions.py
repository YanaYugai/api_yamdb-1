from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request

from users.models import User


class IsAdmin(BasePermission):
    """Разрешение для управления пользоватклями."""

    def has_permission(self, request: Request, view: None) -> bool:
        del view
        return request.user.is_authenticated and (
            request.user.role == User.ADMIN or request.user.is_superuser
        )

    def has_object_permission(self, request: Request, view: None, obj) -> bool:
        del view, obj
        return request.user.is_superuser or request.user.role == User.ADMIN


# Категории, Жанры, Тайтлы(после использования - стереть)
class IsAdminOrReadOnly(BasePermission):
    """Разрешение редактирования только Админу."""

    def has_permission(self, request: Request, view: None) -> bool:
        del view
        return (
            request.method in SAFE_METHODS or request.user.role == User.ADMIN
        )

    def has_object_permission(self, request: Request, view: None, obj) -> bool:
        del view, obj
        return request.user.is_authenticated and (
            request.user.role == User.ADMIN or request.user.is_superuser
        )


# для Review и comments(после использования - стереть)
class IsUserAdminAuthorModeratorOrReadOnly(BasePermission):
    """Разрешение редактирования только Админу, Автору и Модератору."""

    def has_permission(self, request: Request, view: None) -> bool:
        del view
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request: Request, view: None, obj) -> bool:
        del view
        return (
            obj.author == request.user
            or request.user.role == User.MODERATOR
            or request.user.role == User.ADMIN
            or request.user.is_superuser
        )
