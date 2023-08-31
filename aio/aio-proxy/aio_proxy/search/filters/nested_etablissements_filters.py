from aio_proxy.search.helpers.elastic_fields import get_elasticsearch_field_name


def build_etablissements_filters(search_params):
    """Three types of searches are implemented to filter `établissements` values:

    1. Filter search by exact matches on text values,
        e.g. : "departement", "code_postal", "commune", "region"

    2. Filter search by matching an id in an array of ids,
        e.g. ids : "id_convention_collective",
                  "id_uai",
                  "id_finess",
                  "id_rge",

    3. Filter search by bool parameters,
    The parameters relevant to this filter are variables that have both bool values
    indexed in `unité légale` and a list of values indexed in `établissements`
    e.g "convention_collective_renseignee" -> "liste_idcc",
        "est_bio" -> "liste_id_bio",
        "est_finess" -> "liste_finess",
        "est_uai" -> "liste_uai",
        "est_entrepreneur_spectacle" -> "est_entrepreneur_spectacle",
        "est_rge" -> "est_rge",
    """

    # Id filters are used in the `should` clause
    id_filters = ["id_finess", "id_rge", "id_uai", "id_convention_collective"]
    # Text filters are used in the `must` clause
    text_filters = ["departement", "code_postal", "commune", "region"]
    # Bool filters are used in both `must` and `must_not` clauses depending on the
    # filter value
    bool_filters = [
        "convention_collective_renseignee",
        "est_finess",
        "est_bio",
        "est_uai",
        "est_rge",
    ]

    terms_filters = []
    must_filters = []
    must_not_filters = []

    # params is the list of parameters (filters) provided in the request
    for param_name, param_value in vars(search_params).items():
        should_apply_text_filter = (
            param_value is not None and param_name in text_filters
        )
        if should_apply_text_filter:
            terms_filters.append(
                {
                    "terms": {
                        "unite_legale.etablissements." + param_name: param_value,
                    }
                }
            )
        should_apply_id_filter = param_value is not None and param_name in id_filters
        if should_apply_id_filter:
            field = get_elasticsearch_field_name(param_name)
            must_filters.append(
                {
                    "match": {
                        "unite_legale.etablissements."
                        + field: {
                            "query": param_value,
                            "_name": "Filter id:" + field,
                        }
                    }
                }
            )
        should_apply_bool_filter = (
            param_value is not None and param_name in bool_filters
        )
        # These filters are applied in cases like "est_rge", where the filter should
        # be applied to both `unité légale` and `établissements`
        # The `must exists`clause is applied when the filter value is `True`, and the
        # `must_not exists` when the value is `False`
        if should_apply_bool_filter:
            field = get_elasticsearch_field_name(param_name)
            if param_value:
                must_filters.append(
                    {"exists": {"field": "unite_legale.etablissements." + field}}
                )
            else:
                must_not_filters.append(
                    {"exists": {"field": "unite_legale.etablissements." + field}}
                )
    return terms_filters, must_filters, must_not_filters


def build_nested_etablissements_filters_query(search_params, with_inner_hits=False):
    filters_query = {
        "nested": {
            "path": "unite_legale.etablissements",
            "query": {"bool": {}},
        }
    }

    (
        terms_filters,
        must_filters,
        must_not_filters,
    ) = build_etablissements_filters(search_params)

    if not (terms_filters or must_filters or must_not_filters):
        return None

    if terms_filters:
        filters_query["nested"]["query"]["bool"]["filter"] = terms_filters
    if must_filters:
        filters_query["nested"]["query"]["bool"]["must"] = must_filters
    if must_not_filters:
        filters_query["nested"]["query"]["bool"]["must_not"] = must_not_filters

    if with_inner_hits:
        filters_query["nested"]["inner_hits"] = {
            "size": search_params.matching_size,
            "sort": {
                "unite_legale.etablissements.etat_administratif": {"order": "asc"}
            },
        }

    return filters_query


def add_nested_etablissements_filters_to_text_query(text_query, search_params):
    (
        terms_filters,
        must_filters,
        must_not_filters,
    ) = build_etablissements_filters(search_params)
    # Number `5` corresponds to the index of the nested query in the text query
    # every time a new query is added to the text query before the nested query,
    # this index should be modified to reflect that change
    if terms_filters:
        text_query["bool"]["should"][6]["function_score"]["query"]["nested"]["query"][
            "bool"
        ]["filter"] = terms_filters
    if must_filters:
        text_query["bool"]["should"][6]["function_score"]["query"]["nested"]["query"][
            "bool"
        ]["must"] = must_filters
    if must_not_filters:
        text_query["bool"]["should"][6]["function_score"]["query"]["nested"]["query"][
            "bool"
        ]["must_not"] = must_not_filters
    return text_query
