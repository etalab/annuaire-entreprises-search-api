from aio_proxy.search.filters.boolean import (
    filter_search_by_bool_fields_unite_legale,
    filter_search_by_bool_nested_fields_unite_legale,
)
from aio_proxy.search.filters.nested_etablissements_filters import (
    add_nested_etablissements_filters_to_text_query,
    build_nested_etablissements_filters_query,
)
from aio_proxy.search.filters.siren import filter_by_siren
from aio_proxy.search.filters.siret import filter_by_siret
from aio_proxy.search.filters.term_filters import (
    filter_term_list_search_unite_legale,
    filter_term_search_unite_legale,
)
from aio_proxy.search.helpers.bilan_filters_used import is_any_bilan_filter_used
from aio_proxy.search.helpers.etablissements_filters_used import (
    is_any_etablissement_filter_used,
)
from aio_proxy.search.parsers.siren import is_siren
from aio_proxy.search.parsers.siret import is_siret
from aio_proxy.search.queries.bilan import search_bilan
from aio_proxy.search.queries.person import search_person
from aio_proxy.search.queries.text import build_text_query
from elasticsearch_dsl import Q


def text_search(es_search_builder):
    query_terms = es_search_builder.search_params.terms
    # Filter by siren/siret first (if query is a `siren` or 'siret' number),
    # and return search results directly without text search.
    if is_siren(query_terms) or is_siret(query_terms):
        query_terms_clean = query_terms.replace(" ", "")
        if is_siren(query_terms):
            es_search_builder.es_search_client = filter_by_siren(
                es_search_builder.es_search_client, query_terms_clean
            )
        else:
            es_search_builder.es_search_client = filter_by_siret(
                es_search_builder.es_search_client, query_terms_clean
            )
    else:
        # Always apply this filter for text search to prevent displaying
        # non-diffusible data
        es_search_builder.es_search_client = es_search_builder.es_search_client.filter(
            "term", **{"statut_diffusion_unite_legale": "O"}
        )
        # Filter results by term using 'unité légale' related filters in the request
        es_search_builder.es_search_client = filter_term_search_unite_legale(
            es_search_builder.es_search_client,
            es_search_builder.search_params,
            filters_to_include=[
                "convention_collective_renseignee",
                "economie_sociale_solidaire_unite_legale",
                "egapro_renseignee",
                "est_bio",
                "est_entrepreneur_individuel",
                "est_entrepreneur_spectacle",
                "est_finess",
                "est_organisme_formation",
                "est_qualiopi",
                "est_rge",
                "est_service_public",
                "est_uai",
                "etat_administratif_unite_legale",
                "est_societe_mission",
            ],
        )

        # Filter results by list of terms, using 'unité légale' related list
        # of values
        es_search_builder.es_search_client = filter_term_list_search_unite_legale(
            es_search_builder.es_search_client,
            es_search_builder.search_params,
            filters_to_include=[
                "activite_principale_unite_legale",
                "code_collectivite_territoriale",
                "nature_juridique_unite_legale",
                "section_activite_principale",
                "tranche_effectif_salarie_unite_legale",
                "categorie_entreprise",
            ],
        )

        # Boolean filters for unité légale
        es_search_builder.es_search_client = filter_search_by_bool_fields_unite_legale(
            es_search_builder.es_search_client,
            es_search_builder.search_params,
            filters_to_include=[
                "est_association",
                "est_collectivite_territoriale",
            ],
        )

        # Boolean nested field filters unite_legale
        # For now, only use for bilan_financier object
        es_search_builder.es_search_client = (
            filter_search_by_bool_nested_fields_unite_legale(
                es_search_builder.es_search_client,
                es_search_builder.search_params,
                filters_to_include=[
                    "bilan_renseigne",
                ],
                path="bilan_financier",
            )
        )

        # Check if any etablissements filters are used
        etablissement_filter_used = is_any_etablissement_filter_used(
            es_search_builder.search_params
        )

        if etablissement_filter_used:
            # Filters applied on établissements, 1st application of filters
            # before text search to make sure the text_query (on unite légale) is
            # applied only to filtered results.
            # Otherwise, the text_query (with filters injected) will return all
            # unite legale that match the filter without any regarde to the
            # text_query on unite_legale These filters are applied always,
            # even with a query search, since we do not include inner hits in
            # this particular search query
            filters_etablissements_query_without_inner_hits = (
                build_nested_etablissements_filters_query(
                    es_search_builder.search_params, with_inner_hits=False
                )
            )
            if filters_etablissements_query_without_inner_hits:
                es_search_builder.es_search_client = (
                    es_search_builder.es_search_client.query(
                        Q(filters_etablissements_query_without_inner_hits)
                    )
                )

            # Filters applied on établissement with text search
            if query_terms:
                text_query = build_text_query(
                    terms=query_terms,
                    matching_size=es_search_builder.search_params.matching_size,
                )
                text_query_with_filters = (
                    add_nested_etablissements_filters_to_text_query(
                        text_query, es_search_builder.search_params
                    )
                )
                es_search_builder.es_search_client = (
                    es_search_builder.es_search_client.query(Q(text_query_with_filters))
                )

            # Filters applied on établissements without text search
            else:
                filters_etablissements_query_with_inner_hits = (
                    build_nested_etablissements_filters_query(
                        es_search_builder.search_params, with_inner_hits=True
                    )
                )
                if filters_etablissements_query_with_inner_hits:
                    es_search_builder.es_search_client = (
                        es_search_builder.es_search_client.query(
                            Q(filters_etablissements_query_with_inner_hits)
                        )
                    )
        else:
            # Text search only without etablissements filters
            if query_terms:
                text_query = build_text_query(
                    terms=query_terms,
                    matching_size=es_search_builder.search_params.matching_size,
                )
                es_search_builder.es_search_client = (
                    es_search_builder.es_search_client.query(Q(text_query))
                )

        # Search by chiffre d'affaire or resultat net in bilan_financier
        is_bilan_bilan_used = is_any_bilan_filter_used(es_search_builder.search_params)
        if is_bilan_bilan_used:
            es_search_builder.es_search_client = search_bilan(
                es_search_builder.es_search_client,
                es_search_builder.search_params,
                bilan_filters_to_include=[
                    "ca_min",
                    "ca_max",
                    "resultat_net_min",
                    "resultat_net_max",
                ],
            )

        # Search 'élus' only
        type_personne = es_search_builder.search_params.type_personne
        if type_personne == "ELU":
            es_search_builder.es_search_client = search_person(
                es_search_builder.es_search_client,
                es_search_builder.search_params,
                "nom_personne",
                "prenoms_personne",
                "min_date_naiss_personne",
                "max_date_naiss_personne",
                [
                    {
                        "type_person": "colter_elus",
                        "match_nom": "nom",
                        "match_prenom": "prenom",
                        "match_date": "date_naissance",
                    },
                ],
            )
        # Search 'dirigeants' only
        elif type_personne == "DIRIGEANT":
            es_search_builder.es_search_client = search_person(
                es_search_builder.es_search_client,
                es_search_builder.search_params,
                "nom_personne",
                "prenoms_personne",
                "min_date_naiss_personne",
                "max_date_naiss_personne",
                [
                    {
                        "type_person": "dirigeants_pp",
                        "match_nom": "nom",
                        "match_prenom": "prenoms",
                        "match_date": "date_naissance",
                    },
                ],
            )
        else:
            # Search both 'élus' and 'dirigeants'
            es_search_builder.es_search_client = search_person(
                es_search_builder.es_search_client,
                es_search_builder.search_params,
                "nom_personne",
                "prenoms_personne",
                "min_date_naiss_personne",
                "max_date_naiss_personne",
                [
                    {
                        "type_person": "dirigeants_pp",
                        "match_nom": "nom",
                        "match_prenom": "prenoms",
                        "match_date": "date_naissance",
                    },
                    {
                        "type_person": "colter_elus",
                        "match_nom": "nom",
                        "match_prenom": "prenom",
                        "match_date": "date_naissance",
                    },
                ],
            )

        # Sorting is only applied for text queries and not filters
        for item in [
            "terms",
            "nom_personne",
            "prenoms_personne",
        ]:
            if getattr(es_search_builder.search_params, item):
                es_search_builder.is_text_search = True

        # By default, exclude etablissements list from response
        if not es_search_builder.search_params.inclure_etablissements:
            es_search_builder.es_search_client = (
                es_search_builder.es_search_client.source(excludes=["etablissements"])
            )
