from aio_proxy.request.helpers import validate_date_range
from aio_proxy.request.parsers.activite_principale import validate_activite_principale
from aio_proxy.request.parsers.ban_params import ban_params
from aio_proxy.request.parsers.bool_fields import parse_and_validate_bool_field
from aio_proxy.request.parsers.categorie_entreprise import validate_categorie_entreprise
from aio_proxy.request.parsers.code_commune import validate_code_commune
from aio_proxy.request.parsers.code_postal import validate_code_postal
from aio_proxy.request.parsers.collectivite_territoriale import (
    validate_code_collectivite_territoriale,
)
from aio_proxy.request.parsers.convention_collective import (
    validate_id_convention_collective,
)
from aio_proxy.request.parsers.date_parser import parse_and_validate_date
from aio_proxy.request.parsers.departement import validate_departement
from aio_proxy.request.parsers.empty_params import check_empty_params
from aio_proxy.request.parsers.etat_administratif import validate_etat_administratif
from aio_proxy.request.parsers.finess import validate_id_finess
from aio_proxy.request.parsers.insee_bool import match_bool_to_insee_value
from aio_proxy.request.parsers.int_parser import parse_and_validate_int
from aio_proxy.request.parsers.latitude import parse_and_validate_latitude
from aio_proxy.request.parsers.longitude import parse_and_validate_longitude
from aio_proxy.request.parsers.matching_size import parse_and_validate_matching_size
from aio_proxy.request.parsers.nature_juridique import validate_nature_juridique
from aio_proxy.request.parsers.page import parse_and_validate_page
from aio_proxy.request.parsers.per_page import parse_and_validate_per_page
from aio_proxy.request.parsers.radius import parse_and_validate_radius
from aio_proxy.request.parsers.rge import validate_id_rge
from aio_proxy.request.parsers.section_activite_principale import (
    validate_section_activite_principale,
)
from aio_proxy.request.parsers.string_parser import clean_parameter, parse_parameter
from aio_proxy.request.parsers.terms import (
    check_short_terms_and_no_param,
    parse_and_validate_terms,
)
from aio_proxy.request.parsers.tranche_effectif import validate_tranche_effectif_salarie
from aio_proxy.request.parsers.type_personne import validate_type_personne
from aio_proxy.request.parsers.uai import validate_id_uai
from aio_proxy.request.search_params_model import SearchParams
from aio_proxy.utils.utils import str_to_list


class SearchParamsBuilder:
    """This class extracts parameter values from request and saves them in a
    SearchParams dataclass object."""

    @staticmethod
    def get_text_search_params(request):
        params = SearchParams(
            page=parse_and_validate_page(request),
            per_page=parse_and_validate_per_page(request),
            terms=parse_and_validate_terms(request),
            matching_size=parse_and_validate_matching_size(request),
            inclure_score=parse_and_validate_bool_field(request, param="inclure_score"),
            inclure_slug=parse_and_validate_bool_field(request, param="inclure_slug"),
            inclure_etablissements=parse_and_validate_bool_field(
                request, param="inclure_etablissements"
            ),
            nature_juridique_unite_legale=validate_nature_juridique(
                str_to_list(clean_parameter(request, param="nature_juridique"))
            ),
            id_rge=validate_id_rge(clean_parameter(request, param="id_rge")),
            nom_personne=parse_parameter(request, param="nom_personne"),
            prenoms_personne=parse_parameter(request, param="prenoms_personne"),
            min_date_naiss_personne=parse_and_validate_date(
                request, param="date_naissance_personne_min"
            ),
            max_date_naiss_personne=parse_and_validate_date(
                request, param="date_naissance_personne_max"
            ),
            ca_min=parse_and_validate_int(request, param="ca_min"),
            ca_max=parse_and_validate_int(request, param="ca_max"),
            resultat_net_min=parse_and_validate_int(request, param="resultat_net_min"),
            resultat_net_max=parse_and_validate_int(request, param="resultat_net_max"),
            type_personne=validate_type_personne(
                clean_parameter(request, param="type_personne")
            ),
            etat_administratif_unite_legale=validate_etat_administratif(
                clean_parameter(request, param="etat_administratif")
            ),
            activite_principale_unite_legale=validate_activite_principale(
                str_to_list(clean_parameter(request, param="activite_principale"))
            ),
            bilan_renseigne=parse_and_validate_bool_field(
                request, param="bilan_renseigne"
            ),
            categorie_entreprise=validate_categorie_entreprise(
                str_to_list(clean_parameter(request, param="categorie_entreprise"))
            ),
            commune=validate_code_commune(
                str_to_list(clean_parameter(request, param="code_commune"))
            ),
            code_postal=validate_code_postal(
                str_to_list(clean_parameter(request, param="code_postal"))
            ),
            departement=validate_departement(
                str_to_list(clean_parameter(request, param="departement"))
            ),
            est_entrepreneur_individuel=parse_and_validate_bool_field(
                request, param="est_entrepreneur_individuel"
            ),
            section_activite_principale=validate_section_activite_principale(
                str_to_list(
                    clean_parameter(request, param="section_activite_principale")
                )
            ),
            tranche_effectif_salarie_unite_legale=validate_tranche_effectif_salarie(
                str_to_list(clean_parameter(request, param="tranche_effectif_salarie"))
            ),
            convention_collective_renseignee=parse_and_validate_bool_field(
                request, param="convention_collective_renseignee"
            ),
            egapro_renseignee=parse_and_validate_bool_field(
                request, param="egapro_renseignee"
            ),
            est_bio=parse_and_validate_bool_field(request, param="est_bio"),
            est_finess=parse_and_validate_bool_field(request, param="est_finess"),
            est_uai=parse_and_validate_bool_field(request, param="est_uai"),
            est_collectivite_territoriale=parse_and_validate_bool_field(
                request, param="est_collectivite_territoriale"
            ),
            est_entrepreneur_spectacle=parse_and_validate_bool_field(
                request, param="est_entrepreneur_spectacle"
            ),
            est_association=parse_and_validate_bool_field(
                request, param="est_association"
            ),
            est_organisme_formation=parse_and_validate_bool_field(
                request, param="est_organisme_formation"
            ),
            est_qualiopi=parse_and_validate_bool_field(request, param="est_qualiopi"),
            est_rge=parse_and_validate_bool_field(request, param="est_rge"),
            est_service_public=parse_and_validate_bool_field(
                request, param="est_service_public"
            ),
            est_societe_mission=match_bool_to_insee_value(
                parse_and_validate_bool_field(request, param="est_societe_mission"),
            ),
            economie_sociale_solidaire_unite_legale=match_bool_to_insee_value(
                parse_and_validate_bool_field(request, param="est_ess"),
            ),
            id_convention_collective=validate_id_convention_collective(
                clean_parameter(request, param="id_convention_collective")
            ),
            id_finess=validate_id_finess(clean_parameter(request, param="id_finess")),
            id_uai=validate_id_uai(clean_parameter(request, param="id_uai")),
            code_collectivite_territoriale=validate_code_collectivite_territoriale(
                str_to_list(
                    clean_parameter(request, param="code_collectivite_territoriale")
                )
            ),
        )
        SearchParamsBuilder.check_and_validate_params(request, params)
        return params

    @staticmethod
    def get_geo_search_params(request):
        params = SearchParams(
            page=parse_and_validate_page(request),
            per_page=parse_and_validate_per_page(request),
            lat=parse_and_validate_latitude(request),
            lon=parse_and_validate_longitude(request),
            radius=parse_and_validate_radius(request),
            activite_principale_unite_legale=validate_activite_principale(
                str_to_list(clean_parameter(request, param="activite_principale"))
            ),
            section_activite_principale=validate_section_activite_principale(
                str_to_list(
                    clean_parameter(request, param="section_activite_principale")
                )
            ),
            inclure_etablissements=parse_and_validate_bool_field(
                request, param="inclure_etablissements"
            ),
            inclure_slug=parse_and_validate_bool_field(request, param="inclure_slug"),
            inclure_score=parse_and_validate_bool_field(request, param="inclure_score"),
            matching_size=parse_and_validate_matching_size(request),
        )
        return params

    @staticmethod
    def check_and_validate_params(request, params):
        check_empty_params(params)
        ban_params(request, "localisation")
        validate_date_range(
            params.min_date_naiss_personne,
            params.max_date_naiss_personne,
        )
        # Prevent performance issues by refusing query terms less than 3 characters
        # unless another param is provided
        check_short_terms_and_no_param(params)
