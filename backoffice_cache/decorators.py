import functools
from typing import Literal

from rest_framework.request import Request
from rest_framework.response import Response

from backoffice_cache.services import CacheService


def get_cache_key(request: Request) -> str:
    authorization = request.META.get("HTTP_AUTHORIZATION")
    return authorization


def set_cache_response():

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            cache_key = get_cache_key(request=request)
            cache_service = CacheService()
            response = view_func(self, request, *args, **kwargs)
            if isinstance(response, Response):
                cache_service.set_response_cache_data(
                    cache_key=cache_key,
                    response_data=response.data
                )
            return response
        return wrapper
    return decorator
