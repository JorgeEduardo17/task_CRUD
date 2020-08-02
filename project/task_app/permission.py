from rest_framework.permissions import BasePermission


class IsUserOwnerTAskAuthenticated(BasePermission):
    """
    Allows access only to authenticated users and owner task.
    """

    def has_object_permission(self, request, view, obj):
        task = obj
        if (request.user == task.user) and request.user.is_authenticated:
            return True
        return False
