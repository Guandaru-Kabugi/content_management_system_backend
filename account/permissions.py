# account/permissions.py
from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    message = "Only super admins are allowed to perform this action."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return (
            user.is_staff is True and
            user.role == "superadmin"
        )
