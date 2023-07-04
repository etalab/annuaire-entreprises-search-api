from aio_proxy.search.es_index import ElasticsearchSireneIndex


class ElasticSearchBuilder:
    def __init__(self, search_params):
        self.es_search_client = ElasticsearchSireneIndex.search()
        self.search_params = search_params
        self.total_results = None
        self.execution_time = None
        self.es_response = None

    def sort_text_search(self):
        # Sorting is very heavy on performance if there are no
        # search terms (only filters). As there is no search terms, we can
        # exclude this sorting because score is the same for all results
        # documents. Beware, nom and prenoms are search fields.
        self.es_search_client = self.es_search_client.sort(
            {"_score": {"order": "desc"}},
            {"etat_administratif_unite_legale": {"order": "asc"}},
        )

    def sort_only_filters(self):
        # If only filters are used, use nombre établissements ouverts to sort the
        # results
        self.es_search_client = self.es_search_client.sort(
            {"nombre_etablissements_ouverts": {"order": "desc"}},
        )

    def aggregate_by_siren(self):
        # Collapse is used to aggregate the results by siren. It is the consequence of
        # separating large documents into smaller ones
        self.es_search_client = self.es_search_client.update_from_dict(
            {"collapse": {"field": "siren"}}
        )

    def page_through_results(self):
        size = self.search_params.per_page
        offset = self.search_params.page * size
        return self.es_search_client[offset : (offset + size)]

    def execute_and_agg_total_results_by_siren(self):
        self.es_search_client.aggs.metric("by_cluster", "cardinality", field="siren")
        self.page_through_results()
        self.es_search_client.execute()
        self.total_results = self.es_search_client.aggregations.by_cluster.value
        self.execution_time = self.es_search_client.took

    def execute_es(self):
        self.es_search_client = self.page_through_results
        self.es_response = self.es_search_client.execute()
        self.total_results = self.es_response.hits.total.value
        self.execution_time = self.es_response.took

    def track_scores(self):
        self.es_search_client = self.es_search_client.extra(
            track_scores=True, explain=True
        )
