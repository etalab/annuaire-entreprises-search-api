from aio_proxy.response.formatters.enseignes import format_enseignes
from aio_proxy.response.helpers import get_value
from aio_proxy.response.unite_legale_model import UniteLegaleEtablissement


def format_etablissement(source_etablissement):
    def get_field(field, default=None):
        return get_value(source_etablissement, field, default)

    formatted_etablissement = {
        "activite_principale": get_field("activite_principale"),
        "activite_principale_registre_metier": get_field(
            "activite_principale_registre_metier"
        ),
        "adresse": get_field("adresse"),
        "cedex": get_field("cedex"),
        "code_pays_etranger": get_field("code_pays_etranger"),
        "code_postal": get_field("code_postal"),
        "commune": get_field("commune"),
        "complement_adresse": get_field("complement_adresse"),
        "coordonnees": get_field("coordonnees"),
        "date_creation": get_field("date_creation"),
        "date_debut_activite": get_field("date_debut_activite"),
        "departement": get_field("departement"),
        "distribution_speciale": get_field("distribution_speciale"),
        "est_siege": get_field("est_siege"),
        "etat_administratif": get_field("etat_administratif"),
        "geo_adresse": get_field("geo_adresse"),
        "geo_id": get_field("geo_id"),
        "indice_repetition": get_field("indice_repetition"),
        "latitude": get_field("latitude"),
        "libelle_cedex": get_field("libelle_cedex"),
        "libelle_commune": get_field("libelle_commune"),
        "libelle_commune_etranger": get_field("libelle_commune_etranger"),
        "libelle_pays_etranger": get_field("libelle_pays_etranger"),
        "libelle_voie": get_field("libelle_voie"),
        "liste_enseignes": format_enseignes(
            [
                get_field("enseigne_1"),
                get_field("enseigne_2"),
                get_field("enseigne_3"),
            ]
        ),
        "liste_finess": get_field("liste_finess"),
        "liste_id_bio": get_field("liste_id_bio"),
        "liste_idcc": get_field("liste_idcc"),
        "liste_id_organisme_formation": get_field("liste_id_organisme_formation"),
        "liste_rge": get_field("liste_rge"),
        "liste_uai": get_field("liste_uai"),
        "longitude": get_field("longitude"),
        "nom_commercial": get_field("nom_commercial"),
        "numero_voie": get_field("numero_voie"),
        "region": get_field("region"),
        "siret": get_field("siret"),
        "tranche_effectif_salarie": get_field("tranche_effectif_salarie"),
        "type_voie": get_field("type_voie"),
    }
    return UniteLegaleEtablissement(**formatted_etablissement)


def format_etablissements_list(etablissements=None):
    hidden_fields = [
        "activite_principale_registre_metier",
        "coordonnees",
        "cedex",
        "code_pays_etranger",
        "complement_adresse",
        "departement",
        "distribution_speciale",
        "geo_adresse",
        "indice_repetition",
        "libelle_cedex",
        "libelle_commune_etranger",
        "libelle_pays_etranger",
        "libelle_voie",
        "numero_voie",
        "tranche_effectif_salarie",
        "type_voie",
    ]
    etablissements_formatted = []
    if etablissements:
        for etablissement in etablissements:
            etablissement_formatted = format_etablissement(etablissement).dict()
            # Hide certain fields from response to avoid bulky response
            for field in hidden_fields:
                del etablissement_formatted[field]
            etablissements_formatted.append(
                UniteLegaleEtablissement(**etablissement_formatted)
            )
    return etablissements_formatted


def format_siege(siege=None):
    siege_formatted = format_etablissement(siege).dict()
    return UniteLegaleEtablissement(**siege_formatted)
