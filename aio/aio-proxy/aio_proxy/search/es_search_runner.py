import logging
from datetime import timedelta

from aio_proxy.request.search_type import SearchType
from aio_proxy.search.es_search_builder import ElasticSearchBuilder
from aio_proxy.search.geo_search import build_es_search_geo_query
from aio_proxy.search.helpers.helpers import extract_ul_and_etab_from_es_response
from aio_proxy.search.text_search import build_es_search_text_query
from aio_proxy.utils.cache import cache_strategy

TIME_TO_LIVE = timedelta(days=31)
MIN_EXECUTION_TIME = 400
MAX_TOTAL_RESULTS = 10000


class ElasticSearchRunner:
    def __init__(self, search_params, search_type):
        self.es_search_builder = ElasticSearchBuilder(search_params)
        # self.es_search_client = self.es_search_builder.es_search_client
        self.search_type = search_type
        self.has_full_text_query = False
        self.es_search_results = None
        self.total_results = None
        self.execution_time = None
        self.run()

    def sort_es_search_query(self):
        if self.has_full_text_query:
            self.es_search_builder.sort_text_search()
        else:
            self.es_search_builder.sort_only_filters()

    def execute_and_format_es_search(self):
        self.es_search_builder.execute_es()
        # Due to performance issues when aggregating on filter queries, we use
        # aggregation on total_results only when total_results is lower than
        # 10 000 results. If total_results is higher than 10 000 results,
        # the aggregation causes timeouts on API. We return by default 10 000 results.
        max_results_exceeded = self.es_search_builder.total_results >= MAX_TOTAL_RESULTS
        if not max_results_exceeded:
            self.es_search_builder.execute_and_agg_total_results_by_siren()

        self.es_search_results = []
        for matching_unite_legale in self.es_search_builder.es_response.hits:
            matching_unite_legale_dict = extract_ul_and_etab_from_es_response(
                matching_unite_legale
            )
            self.es_search_results.append(matching_unite_legale_dict)
        self.total_results = self.es_search_builder.total_results
        self.execution_time = self.es_search_builder.execution_time
        logging.info(f"/////// total results{self.total_results}")
        logging.info(f"/////// total execution_time{self.execution_time}")

    def sort_and_execute_es_search_query(self):
        self.es_search_builder.track_scores()
        self.es_search_builder.aggregate_by_siren()
        # Sort results
        self.sort_es_search_query()

        # Execute search, only called if key not found in cache
        # (see cache strategy below)
        def get_es_search_response():
            self.execute_and_format_es_search()
            es_results_to_cache = {
                "total_results": self.total_results,
                "response": self.es_search_results,
                "execution_time": self.execution_time,
            }
            return es_results_to_cache

        # To make sure the page and page size are part of the cache key
        cache_key = self.es_search_builder.page_through_results()

        cached_search_results = cache_strategy(
            cache_key,
            get_es_search_response,
            self.should_cache_search_response,
            TIME_TO_LIVE,
        )

        self.total_results = cached_search_results["total_results"]
        self.es_search_results = cached_search_results["response"]
        self.execution_time = cached_search_results["execution_time"]

    def should_cache_search_response(self):
        """Cache search response if execution time is higher than 400 ms"""
        try:
            if self.execution_time > MIN_EXECUTION_TIME:
                return True
            return False
        except KeyError as error:
            logging.info(f"Error getting search execution time: {error}")
            return False

    def run(self):
        if self.search_type == SearchType.TEXT:
            build_es_search_text_query(self.es_search_builder)
        elif self.search_type == SearchType.GEO:
            build_es_search_geo_query(self.es_search_builder)
        self.sort_and_execute_es_search_query()
