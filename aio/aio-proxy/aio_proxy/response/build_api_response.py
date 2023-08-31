import json

from aio_proxy.decorators.http_exception import http_exception_handler
from aio_proxy.request.search_params_builder import SearchParamsBuilder
from aio_proxy.response.response_builder import ResponseBuilder
from aio_proxy.search.es_search_runner import ElasticSearchRunner
from aiohttp import web


@http_exception_handler
def build_api_response(
    request,
    search_type,
) -> dict[str, int]:
    """Create and format API response.

    Args:
        request: HTTP request.
        search_type: type of search.
    Returns:
        response in json format (results, total_results, page, per_page,
        total_pages)
    """
    search_params = SearchParamsBuilder.extract_params(request, search_type)
    es_search_results = ElasticSearchRunner(search_params, search_type)
    formatted_response = ResponseBuilder(search_params, es_search_results)
    return web.json_response(text=json.dumps(formatted_response.response, default=str))
