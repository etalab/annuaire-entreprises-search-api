import json
import logging
from collections.abc import Callable

from aio_proxy.decorators.http_exception import http_exception_handler
from aio_proxy.response.format_response import format_response
from aio_proxy.response.format_search_results import format_search_results
from aio_proxy.search.es_index import ElasticsearchSireneIndex
from aio_proxy.search.es_search_runner import ElasticSearchRunner
from aiohttp import web
from sentry_sdk import capture_exception, push_scope


@http_exception_handler
def api_response(
    request,
    extract_function: Callable,
    search_type: str,
) -> dict[str, int]:
    """Create and format API response.

    Args:
        request: HTTP request.
        extract_function (Callable): function used to extract parameters.
        search_type (Callable): type of search (text or geo).
    Returns:
        response in json format (results, total_results, page, per_page,
        total_pages)
    """
    try:
        search_params = extract_function(request)
        es_search_results = ElasticSearchRunner(
            ElasticsearchSireneIndex, search_params, search_type
        )
        total_results = es_search_results.total_results
        results = es_search_results.es_search_results
        execution_time = es_search_results.execution_time
        results_formatted = format_search_results(results, search_params)
        response_formatted = format_response(
            results_formatted, total_results, execution_time, search_params
        )
        return web.json_response(text=json.dumps(response_formatted, default=str))
    except ValueError as error:
        with push_scope() as scope:
            # group value errors together based on their response (Bad request)
            scope.fingerprint = ["Bad Request"]
            # capture_exception(error)
            logging.warning(f"Bad request: {error}")
            raise error
    # capture error in Sentry
    except Exception as error:
        # capturing error at this level allows us to get the actual error before it's
        # wrapped in http_exception_handler
        capture_exception(error)
        raise error
