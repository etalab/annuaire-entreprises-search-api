from dataclasses import dataclass


@dataclass
class SearchParams:
    """Class for modelling search parameters"""

    page: int = None
    per_page: int = None
    terms: str = None
    activite_principale_unite_legale: list = None
    categorie_entreprise: list = None
    commune: list = None
    code_postal: list = None
    departement: list = None
    region: list = None
    est_entrepreneur_individuel: str = None
    section_activite_principale: list = None
    tranche_effectif_salarie_unite_legale: list = None
    convention_collective_renseignee: str = None
    egapro_renseignee: str = None
    est_bio: str = None
    est_finess: str = None
    est_uai: str = None
    est_collectivite_territoriale: str = None
    est_entrepreneur_spectacle: str = None
    est_association: str = None
    est_organisme_formation: str = None
    est_qualiopi: str = None
    est_rge: str = None
    est_service_public: str = None
    est_societe_mission: str = None
    economie_sociale_solidaire_unite_legale: str = None
    id_convention_collective: str = None
    id_finess: str = None
    id_uai: str = None
    code_collectivite_territoriale: str = None
    id_rge: str = None
    nom_personne: str = None
    prenoms_personne: str = None
    min_date_naiss_personne: str = None
    max_date_naiss_personne: str = None
    ca_min: str = None
    ca_max: str = None
    resultat_net_min: str = None
    resultat_net_max: str = None
    type_personne: str = None
    etat_administratif_unite_legale: str = None
    nature_juridique_unite_legale: list = None
    matching_size: str = None
    lat: float = None
    lon: float = None
    radius: float = None
    minimal: bool = None
    include: list = None
    include_admin: list = None
    inclure_etablissements: bool = None
    include_association: bool = False
