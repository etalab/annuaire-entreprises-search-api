from pydantic import BaseModel


class AssociationResponse(BaseModel):
    identifiant_association: str | None = None
    titre: str | None = None
    siret: str | None = None
    siren: str | None = None
    date_creation: str | None = None
    numero_voie: str | None = None
    type_voie: str | None = None
    libelle_voie: str | None = None
    code_postal: str | None = None
    commune: str | None = None
    libelle_commune: str | None = None
    complement_adresse: str | None = None
    indice_repetition: str | None = None
    distribution_speciale: str | None = None
    slug: str | None = None
    score: float | None = None
    meta: dict | None = None
