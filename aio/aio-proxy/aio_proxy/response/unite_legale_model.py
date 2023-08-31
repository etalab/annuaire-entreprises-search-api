from pydantic import BaseModel


class UniteLegaleEtablissement(BaseModel):
    activite_principale: str | None = None
    activite_principale_registre_metier: str | None = None
    adresse: str = None
    cedex: str | None = None
    code_pays_etranger: str | None = None
    code_postal: str | None = None
    commune: str | None = None
    complement_adresse: str | None = None
    coordonnees: str | None = None
    date_creation: str = None
    date_debut_activite: str | None = None
    departement: str | None = None
    distribution_speciale: str | None = None
    est_siege: bool = None
    etat_administratif: str = None
    geo_adresse: str | None = None
    geo_id: str | None = None
    indice_repetition: str | None = None
    latitude: str | None = None
    libelle_cedex: str | None = None
    libelle_commune: str | None = None
    libelle_commune_etranger: str | None = None
    libelle_pays_etranger: str | None = None
    libelle_voie: str | None = None
    liste_enseignes: list | None = None
    liste_finess: list | None = None
    liste_id_bio: list | None = None
    liste_idcc: list | None = None
    liste_id_organisme_formation: list | None = None
    liste_rge: list | None = None
    liste_uai: list | None = None
    longitude: str | None = None
    nom_commercial: str | None = None
    numero_voie: str | None = None
    region: str | None = None
    siret: str = None
    tranche_effectif_salarie: str | None = None
    type_voie: str | None = None


class UniteLegaleElu(BaseModel):
    nom: str | None = None
    prenoms: str | None = None
    annee_de_naissance: str | None = None
    fonction: str | None = None
    sexe: str | None = None


class UniteLegaleDirigeantsPM(BaseModel):
    siren: str = None
    denomination: str | None = None
    sigle: str | None = None
    qualite: str | None = None
    type_dirigeant: str = "personne morale"


class UniteLegaleDirigeantsPP(BaseModel):
    nom: str | None = None
    prenoms: str | None = None
    annee_de_naissance: str | None = None
    qualite: str | None = None
    type_dirigeant: str = "personne physique"


class UniteLegaleFinances(BaseModel):
    annee_cloture_exercice: str | None = None
    ca: int | None = None
    resultat_net: int | None = None


class UniteLegaleCollectiviteTerritoriale(BaseModel):
    code: str | None = None
    code_insee: str | None = None
    elus: list[UniteLegaleElu] | None = None
    niveau: str | None = None


class UniteLegaleComplements(BaseModel):
    collectivite_territoriale: UniteLegaleCollectiviteTerritoriale | None = None
    convention_collective_renseignee: bool = None
    egapro_renseignee: bool = None
    est_bio: bool = None
    est_entrepreneur_individuel: bool = None
    est_entrepreneur_spectacle: bool = None
    est_ess: bool = None
    est_finess: bool = None
    est_organisme_formation: bool = None
    est_qualiopi: bool = None
    liste_id_organisme_formation: list | None = None
    est_rge: bool = None
    est_service_public: bool = None
    est_societe_mission: bool = None
    est_uai: bool = None
    identifiant_association: str | None = None
    statut_entrepreneur_spectacle: str | None = None


class UniteLegaleResponse(BaseModel):
    siren: str = None
    nom_complet: str | None = None
    nom_raison_sociale: str | None = None
    sigle: str | None = None
    nombre_etablissements: int = None
    nombre_etablissements_ouverts: int = None
    siege: UniteLegaleEtablissement = None
    activite_principale: str | None = None
    categorie_entreprise: str | None = None
    annee_categorie_entreprise: str | None = None
    date_creation: str | None = None
    date_mise_a_jour: str | None = None
    dirigeants: (list[UniteLegaleDirigeantsPP | UniteLegaleDirigeantsPM]) | None = None
    etat_administratif: str = None
    nature_juridique: str | None = None
    section_activite_principale: str | None = None
    tranche_effectif_salarie: str | None = None
    annee_tranche_effectif_salarie: str | None = None
    statut_diffusion: str = None
    matching_etablissements: list[UniteLegaleEtablissement] | None = None
    etablissements: list[UniteLegaleEtablissement] | None = None
    finances: dict[str, UniteLegaleFinances] | None = None
    complements: UniteLegaleComplements = None
    score: float = None
    slug: str = None
    meta: dict = None
