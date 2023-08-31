from aio_proxy.response.association_model import (
    AssociationResponse,
)
from aio_proxy.response.formatters.bilan_financier import format_bilan
from aio_proxy.response.formatters.collectivite_territoriale import (
    format_collectivite_territoriale,
)
from aio_proxy.response.formatters.complements import format_complements
from aio_proxy.response.formatters.dirigeants import format_dirigeants
from aio_proxy.response.formatters.etablissements import (
    format_etablissements_list,
    format_siege,
)
from aio_proxy.response.formatters.insee_bool import format_insee_bool
from aio_proxy.response.formatters.nom_complet import format_nom_complet
from aio_proxy.response.formatters.non_diffusible import (
    hide_non_diffusible_fields,
)
from aio_proxy.response.helpers import (
    create_admin_fields_to_include,
    create_fields_to_include,
    get_value,
    is_dev_env,
)
from aio_proxy.response.unite_legale_model import (
    UniteLegaleResponse,
)


def format_single_unite_legale(result, search_params):
    result_unite_legale = result["unite_legale"]

    def get_field(field, default=None):
        return result_unite_legale.get(field, default)

    unite_legale_fields = {
        "siren": get_field("siren"),
        "nom_complet": format_nom_complet(
            get_field("nom_complet"),
            get_field("sigle"),
            get_field("denomination_usuelle_1_unite_legale"),
            get_field("denomination_usuelle_2_unite_legale"),
            get_field("denomination_usuelle_3_unite_legale"),
        ),
        "nom_raison_sociale": get_field("nom_raison_sociale"),
        "sigle": get_field("sigle"),
        "nombre_etablissements": int(get_field("nombre_etablissements", default=1)),
        "nombre_etablissements_ouverts": int(
            get_field("nombre_etablissements_ouverts", default=0)
        ),
        "activite_principale": get_field("activite_principale_unite_legale"),
        "categorie_entreprise": get_field("categorie_entreprise"),
        "annee_categorie_entreprise": get_field("annee_categorie_entreprise"),
        "date_creation": get_field("date_creation_unite_legale"),
        "date_mise_a_jour": get_field("date_mise_a_jour_unite_legale"),
        "etat_administratif": get_field("etat_administratif_unite_legale"),
        "nature_juridique": get_field("nature_juridique_unite_legale"),
        "section_activite_principale": get_field("section_activite_principale"),
        "tranche_effectif_salarie": get_field("tranche_effectif_salarie_unite_legale"),
        "annee_tranche_effectif_salarie": get_field("annee_tranche_effectif_salarie"),
        "statut_diffusion": get_field("statut_diffusion_unite_legale"),
    }
    formatted_unite_legale = UniteLegaleResponse(**unite_legale_fields)

    # Some search parameters control fields included in api response
    fields_to_include = create_fields_to_include(
        search_params
    ) + create_admin_fields_to_include(search_params)

    for field in fields_to_include:
        if field == "SIEGE":
            siege = format_siege(get_field("siege"))
            formatted_unite_legale.siege = siege
        if field == "DIRIGEANTS":
            dirigeants = format_dirigeants(
                get_field("dirigeants_pp"),
                get_field("dirigeants_pm"),
            )
            formatted_unite_legale.dirigeants = dirigeants

        if field == "FINANCES":
            finances = format_bilan(get_field("bilan_financier"))
            formatted_unite_legale.finances = finances
        if field == "COMPLEMENTS":
            complements = format_complements(
                collectivite_territoriale=format_collectivite_territoriale(
                    get_field("colter_code"),
                    get_field("colter_code_insee"),
                    get_field("colter_elus"),
                    get_field("colter_niveau"),
                ),
                convention_collective_renseignee=get_field(
                    "convention_collective_renseignee"
                ),
                egapro_renseignee=get_field("egapro_renseignee"),
                est_bio=get_field("est_bio"),
                est_entrepreneur_individuel=get_field(
                    "est_entrepreneur_individuel", default=False
                ),
                est_entrepreneur_spectacle=get_field("est_entrepreneur_spectacle"),
                est_ess=format_insee_bool(
                    get_field("economie_sociale_solidaire_unite_legale")
                ),
                est_finess=get_field("est_finess"),
                est_organisme_formation=get_field("est_organisme_formation"),
                est_qualiopi=get_field("est_qualiopi"),
                liste_id_organisme_formation=get_field("liste_id_organisme_formation"),
                est_rge=get_field("est_rge"),
                est_service_public=get_field("est_service_public"),
                est_societe_mission=format_insee_bool(get_field("est_societe_mission")),
                est_uai=get_field("est_uai"),
                identifiant_association=get_field(
                    "identifiant_association_unite_legale"
                ),
                statut_entrepreneur_spectacle=get_field(
                    "statut_entrepreneur_spectacle",
                ),
            )
            formatted_unite_legale.complements = complements
        if field == "MATCHING_ETABLISSEMENTS":
            matching_etablissements = format_etablissements_list(
                get_value(result, "matching_etablissements")
            )
            formatted_unite_legale.matching_etablissements = matching_etablissements
        if field == "SLUG":
            slug = get_field("slug")
            formatted_unite_legale.slug = slug
        if field == "ETABLISSEMENTS":
            etablissements = format_etablissements_list(get_field("etablissements"))
            formatted_unite_legale.etablissements = etablissements
        if field == "SCORE":
            score = result.get("meta")["score"]
            formatted_unite_legale.score = score
    # Include search score and tree field for dev environment
    if is_dev_env():
        meta = result.get("meta")
        formatted_unite_legale.meta = meta

    # Hide most fields if unité légale is non-diffusible
    is_non_diffusible = (
        True
        if result_unite_legale.get("statut_diffusion_unite_legale") != "O"
        else False
    )
    if is_non_diffusible:
        formatted_unite_legale = hide_non_diffusible_fields(
            formatted_unite_legale.dict(exclude_unset=True)
        )
        return formatted_unite_legale

    # `exclude_unset`` option hides fields which were not
    # explicitly set when creating response object
    return formatted_unite_legale


def format_single_association(result, search_params):
    result_association = result["association"]

    def get_field(field, default=None):
        return result_association.get(field, default)

    association_fields = {
        "identifiant_association": get_field("identifiant_association"),
        "siret": get_field("siret"),
        "siren": get_field("siren"),
        "titre": get_field("titre"),
        "date_creation": get_field("date_creation"),
        "numero_voie": get_field("numero_voie"),
        "type_voie": get_field("type_voie"),
        "libelle_voie": get_field("libelle_voie"),
        "code_postal": get_field("code_postal"),
        "commune": get_field("commune"),
        "libelle_commune": get_field("libelle_commune"),
        "complement_adresse": get_field("complement_adresse"),
        "indice_repetition": get_field("indice_repetition"),
        "distribution_speciale": get_field("distribution_speciale"),
    }
    formatted_association = AssociationResponse(**association_fields)

    # Some search parameters control fields included in api response
    fields_to_include = create_admin_fields_to_include(search_params)
    for field in fields_to_include:
        if field == "SLUG":
            slug = result.get("slug")
            formatted_association.slug = slug
        if field == "SCORE":
            score = result.get("meta")["score"]
            formatted_association.score = score
    # Include search score and tree field for dev environment
    if is_dev_env():
        meta = result.get("meta")
        formatted_association.meta = meta

    return formatted_association


def format_search_results(results, search_params):
    """Main formatting function for all results."""
    formatted_results = []
    for result in results:
        # If structure is unite légale
        if "unite_legale" in result:
            formatted_result = format_single_unite_legale(result, search_params)
            formatted_results.append(formatted_result)
        # If structure is unite légale
        if "association" in result:
            formatted_result = format_single_association(result, search_params)
            formatted_results.append(formatted_result)
    return formatted_results
