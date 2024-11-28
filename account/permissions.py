from rest_framework.permissions import BasePermission


class IsUnauthenticated(BasePermission):
    """
    Allows access only to unauthenticated users.
    """
    
    def has_permission(self, request, view):
        # If the user is authenticated, deny access
        return not request.user.is_authenticated
