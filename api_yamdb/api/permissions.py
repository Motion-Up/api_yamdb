from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права доступа администратора
    (разрешено чтение всем пользователям) """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == 'admin'))

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == 'admin'))


class ModeratorPermission(permissions.BasePermission):
    """Права доступа модератора """

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or (request.user.is_authenticated
                    and request.user.role == 'moderator'))


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Права доступа, позволяющие редактировать только
        владельцам объекта """

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class AuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """Права доступа автора, администратора и модератора"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == 'moderator'
                or request.user.role == 'admin')
