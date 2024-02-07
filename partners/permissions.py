from rest_framework.permissions import BasePermission


class IsServiceAuthenticated(BasePermission):
    """
    Permission class that checks if the request has a 'is_service' attribute.

    This permission class is used to verify if the request has a 'is_service' attribute,
    indicating that the is_service is authenticated. If the 'partner' attribute is present,
    the permission is granted. Otherwise, the permission is denied.

    Note:
        This permission assumes that the authentication process has already been performed
        and has set the 'is_service' attribute on the request
   """

    def has_permission(self, request, view):
        return hasattr(request, 'is_service')
