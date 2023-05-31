from aio_proxy.search.helpers.color import CURRENT_COLOR
from elasticsearch_dsl import Document


class ElasticsearchSireneIndex(Document):
    """

    Model-like class for persisting documents in elasticsearch.
    It's a wrapper around Document to create specific mappings and to add settings in
    elasticsearch.

    Class used to represent a company headquarters,
    one Siren number and the corresponding Siret numbers.

    """

    class Index:
        name = f"siren-{CURRENT_COLOR}"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}
