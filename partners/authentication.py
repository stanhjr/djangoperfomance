from django.contrib.auth.models import AnonymousUser

from rest_framework.authentication import BaseAuthentication

from partners.models import ServiceApiKey


class ServiceApiKeyAuthentication(BaseAuthentication):
    """
    Authenticates the Service Api Key and sets the peer in the request object.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authenticate(self, request, **kwargs):
        authorization = request.META.get('HTTP_AUTHORIZATION')

        if ServiceApiKey.objects.filter(key=authorization).exists():
            request.is_service = True
            return AnonymousUser(), None

    def authenticate_header(self, request) -> str:
        """Return a string that will be used as the value of the WWW-Authenticate header"""
        return "Api-Key"
