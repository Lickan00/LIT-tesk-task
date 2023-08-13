from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOnly(BasePermission):
    """Admin access only."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class ReadOnly(BasePermission):
    """Read-only permission."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAuthorOrModeratorOrReadOnly(BasePermission):
    """
    Permission to change the object only to the moderator, admin or creator.
    Otherwise, it can be read-only.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_moderator
                or request.user.id == obj.pk
            )
        )
