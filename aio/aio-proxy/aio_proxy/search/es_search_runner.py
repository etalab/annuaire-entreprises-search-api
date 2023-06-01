import logging
from datetime import timedelta

from aio_proxy.request.search_type import SearchType
from aio_proxy.search.es_index import ElasticsearchSireneIndex
from aio_proxy.search.geo_search import build_es_search_geo_query
from aio_proxy.search.helpers.helpers import (
    execute_and_agg_total_results_by_siren,
    extract_ul_and_etab_from_es_response,
    page_through_results,
)
from aio_proxy.search.text_search import build_es_search_text_query
from aio_proxy.utils.cache import cache_strategy

TIME_TO_LIVE = timedelta(days=31)
MIN_EXECUTION_TIME = 400
MAX_TOTAL_RESULTS = 10000


class ElasticSearchRunner:
    def __init__(self, search_params, search_type):
        self.es_search_client = ElasticsearchSireneIndex.search()
        self.search_type = search_type
        self.search_params = search_params
        self.has_full_text_query = False
        self.es_search_results = None
        self.total_results = None
        self.execution_time = None
        self.run()

    def sort_es_search_query(self):
        # Sorting is very heavy on performance if there are no
        # search terms (only filters). As there is no search terms, we can
        # exclude this sorting because score is the same for all results
        # documents. Beware, nom and prenoms are search fields.
        if self.has_full_text_query:
            self.es_search_client = self.es_search_client.sort(
                {"_score": {"order": "desc"}},
                {"etat_administratif_unite_legale": {"order": "asc"}},
            )
        # If only filters are used, use nombre établissements ouverts to sort the
        # results
        else:
            self.es_search_client = self.es_search_client.sort(
                {"nombre_etablissements_ouverts": {"order": "desc"}},
            )

    def execute_and_format_es_search(self):
        self.es_search_client = page_through_results(self)
        es_response = self.es_search_client.execute()
        self.total_results = es_response.hits.total.value
        self.execution_time = es_response.took

        # Due to performance issues when aggregating on filter queries, we use
        # aggregation on total_results only when total_results is lower than
        # 10 000 results. If total_results is higher than 10 000 results,
        # the aggregation causes timeouts on API. We return by default 10 000 results.
        max_results_exceeded = self.total_results >= MAX_TOTAL_RESULTS
        if not max_results_exceeded:
            execute_and_agg_total_results_by_siren(self)

        self.es_search_results = []
        for matching_unite_legale in es_response.hits:
            matching_unite_legale_dict = extract_ul_and_etab_from_es_response(
                matching_unite_legale
            )
            self.es_search_results.append(matching_unite_legale_dict)

    def sort_and_execute_es_search_query(self):
        self.es_search_client = self.es_search_client.extra(
            track_scores=True, explain=True
        )
        # Collapse is used to aggregate the results by siren. It is the consequence of
        # separating large documents into smaller ones
        self.es_search_client = self.es_search_client.update_from_dict(
            {"collapse": {"field": "siren"}}
        )
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
        cache_key = page_through_results(self)

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
            build_es_search_text_query(self)
        elif self.search_type == SearchType.GEO:
            build_es_search_geo_query(self)
        self.sort_and_execute_es_search_query()
