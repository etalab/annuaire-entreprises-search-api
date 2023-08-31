from aio_proxy.response.format_search_results import format_search_results
from aio_proxy.response.helpers import is_dev_env
from aio_proxy.response.response_model import ResponseModel


class ResponseBuilder:
    def __init__(self, search_params, es_search_results):
        self.total_results = min(int(es_search_results.total_results), 10000)
        self.per_page = search_params.per_page
        self.results = format_search_results(
            es_search_results.es_search_results, search_params
        )
        self.page = search_params.page + 1
        self.total_pages = self.calculate_total_pages()
        response = ResponseModel(
            results=self.results,
            total_results=self.total_results,
            page=self.page,
            per_page=self.per_page,
            total_pages=self.total_pages,
        )
        if is_dev_env():
            response.execution_time = es_search_results.execution_time
        self.response = response.dict(exclude_unset=True)

    def calculate_total_pages(self):
        quotient, remainder = divmod(
            self.total_results,
            self.per_page,
        )
        total_pages = quotient + 1 if remainder > 0 else quotient
        return total_pages
