import json
from typing import Optional

import redis
from django.conf import settings


class CacheService:
    """
    A service class for interacting with a cache.

    The CacheService provides methods to get, set, and invalidate cache data
    identified by a cache key.

    Args:
        cache_key (str): The key identifying the cache data.
    """

    def __init__(self, cache_key: str = None):
        """
        Initialize a new instance of CacheService.

        Args:
            cache_key (str): The key identifying the cache data.
        """
        self.redis = redis.Redis(
            host=settings.REDIS_HOST_NAME,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )
        self.ttl = settings.REDIS_TTL
        self.cache_key = cache_key

    def get_cache_data(self, cache_key: str) -> Optional[dict | list]:
        """
        Retrieve the cached data associated with the cache key.

        Returns:
            The cached data, or None if the cache key does not exist.
        """
        try:
            data = self.redis.get(cache_key)
            return json.loads(data)
        except TypeError:
            return None

    def set_response_cache_data(self, cache_key: str, response_data: dict | list) -> None:
        """
        Set the cache data associated with the cache key.

        Args:
            cache_key: cache key be stored in the cache.
            response_data: The response data to be stored in the cache.
        Returns:
            None
       """
        json_data = json.dumps(response_data)
        self.redis.set(cache_key, json_data)

    def invalidate_cache_from_pattern(self, pattern: str) -> None:
        """
        Invalidate cache entries matching the specified pattern.

        This method allows you to delete cache entries that match the given pattern.
        It utilizes the 'delete_pattern' function provided by the cache backend to
        perform the deletion. To improve performance and avoid potential performance
        issues, the deletion is done in batches using an optional 'itersize' parameter.

        Parameters:
            pattern (str): A string representing the pattern to match cache keys.

        Returns:
            None: This method does not return any value.
        """

        for key in self.redis.scan_iter(match=pattern, count=10000):
            self.redis.delete(key)

    def invalidate_cache_from_pattern_and_uri(self, pattern: str, uri_list: list) -> None:
        """
        Invalidate cache entries in the Redis database based on a pattern and a list of URIs.

        Args:
            pattern (str): The pattern used for matching cache keys in the Redis database.
            uri_list (list): A list of URIs to append to the pattern for key matching.

        Returns:
            None: This function does not return any value.
        """
        for uri in uri_list:
            pattern_uri = f'{pattern}{uri}*'
            for key in self.redis.scan_iter(match=pattern_uri, count=10000):
                self.redis.delete(key)

    def get_keys_from_pattern(self, pattern: str) -> list:
        """
        Retrieve cache keys matching the specified pattern.

        Used for integration tests!

        This method allows you to get a list of cache keys that match the given pattern.
        It utilizes the 'keys' function provided by the cache backend to perform the
        key retrieval.

        Parameters:
            pattern (str): A string representing the pattern to match cache keys.

        Returns:
            list: A list containing cache keys that match the specified pattern.

        Raises:
            None: This method does not raise any specific exceptions.
        """
        result_list = []
        for key in self.redis.scan_iter(match=pattern, count=10000):
            result_list.append(key.decode('utf-8'))
        return result_list

    def flush_all(self) -> None:
        """
        Flush all cache entries in the Redis database.

        Returns:
            None: This function does not return any value.
        """
        self.redis.flushdb()
