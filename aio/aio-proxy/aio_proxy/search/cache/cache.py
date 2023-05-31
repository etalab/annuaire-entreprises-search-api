import json
import logging
from collections.abc import Callable

from aio_proxy.response.helpers import hash_string
from aio_proxy.search.cache.redis import RedisClient


def build_key(key):
    serialised_key = json.dumps(key.to_dict())
    return hash_string(serialised_key)


def set_cache_value(cache_client, key, value, time_to_live):
    try:
        serialised_value = json.dumps(value, default=str)
        cache_client.set(
            key,
            serialised_value,
            time_to_live,
        )
    except Exception as error:
        logging.info(f"Error while setting value for cache: {error}")


def cache_strategy(
    key,
    get_es_search_response: Callable,
    should_cache_search_response: Callable,
    time_to_live,
):
    try:
        redis_client_cache = RedisClient()
        # Serialize key object before hashing it
        request_cache_key = build_key(key)
        logging.info(f"Request cache key: {request_cache_key}")
        cached_value = redis_client_cache.get(request_cache_key)
        if cached_value:
            return json.loads(cached_value)
        value_to_cache = get_es_search_response()
        should_cache = should_cache_search_response()
        if should_cache:
            set_cache_value(
                redis_client_cache, request_cache_key, value_to_cache, time_to_live
            )
        return value_to_cache
    except Exception as error:
        logging.info(f"Error while trying to cache: {error}")
        return get_es_search_response()
