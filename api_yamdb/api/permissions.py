from rest_framework import permissions



class Admin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin


class ModeratorAuthorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                and request.user.is_moderator)

      
class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_staff
        )


class IsAuthorOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or obj.user == request.user
        )
      