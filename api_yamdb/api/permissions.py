from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_staff
            or request.method in SAFE_METHODS
        )
