from typing import (
    Awaitable,
    Callable,
    List,
    Optional,
)

from django.http import HttpRequest, HttpResponseBase
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from backoffice_cache.services import CacheService


class GetCacheMiddleware(MiddlewareMixin):
    """
    Middleware for caching responses and retrieving cached responses.

    Attributes:
        prefix_cache_list (list): A list of cache prefixes.
        origin_auth (str): The authentication information for the origin.
    """
    prefix_cache_list: List[str] = []
    origin_auth = None

    def __init__(self, get_response: Callable):
        """
        Initializes the GetCacheMiddleware.

        Args:
            get_response (callable): The callable function to get the response.
        """
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponseBase | Awaitable[HttpResponseBase]:
        """
        Handles the incoming request and returns the response.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            HttpResponseBase | Awaitable[HttpResponseBase]: The response.
        """
        return self.process_request(request)

    def _get_cache_key(self, request: HttpRequest) -> str:
        self.origin_auth = request.META.get('HTTP_ORIGIN')
        partner_id = request.META.get('HTTP_PARTNER_ID')
        authorization = request.META.get("HTTP_AUTHORIZATION")
        uri = request.path

        if partner_id and self.origin_auth and not authorization:
            return f'{partner_id}_{self.origin_auth}_{uri}'

        if partner_id and self.origin_auth and authorization:
            return f'{partner_id}_{self.origin_auth}_{authorization}_{uri}'

        if partner_id and authorization:
            return f'{partner_id}_{authorization}_{uri}'

        return authorization

    @staticmethod
    def _is_cached(request: HttpRequest) -> bool:
        """
        Checks if the request's view function has cache settings.

        If the view function has cache settings, it sets the prefix cache list and integration name
        and returns True. Otherwise, it returns False.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            bool: True if the view function has cache settings, False otherwise.
        """

        try:
            view_func: Callable = resolve(request.path_info).func
            if view_func.cls.is_cached:  # type: ignore
                return True
            return False
        except AttributeError:
            return False

    def process_request(self, request: HttpRequest) -> HttpResponseBase | Awaitable[HttpResponseBase]:
        """
        Process the incoming request.

        If the request has cache settings, it checks if there is cached data available.
        If cached data is found, it returns the cached response. Otherwise, it continues
        with the normal request processing.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            HttpResponseBase | Awaitable[HttpResponseBase]: The response.
        """
        if not self._is_cached(request):
            return self.get_response(request)

        cached_data = self._get_cached_data(request=request)

        if cached_data:
            response = Response(cached_data)
            response.accepted_renderer = JSONRenderer()  # type: ignore
            response.accepted_media_type = "application/json"  # type: ignore
            response.renderer_context = {}  # type: ignore
            response.status_code = 200
            if self.origin_auth:
                response["Access-Control-Allow-Origin"] = self.origin_auth
            response.render()
            return response

        return self.get_response(request)

    def _get_cached_data(self, request: HttpRequest) -> Optional[dict | list]:
        """
        Retrieves the cached list data based on the cache prefix and suffix.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            dict: The cached data if found, or None if not found.
        """
        cache_key = self._get_cache_key(request=request)
        if not cache_key:
            return None
        cache_service = CacheService()
        return cache_service.get_cache_data(cache_key=cache_key)
