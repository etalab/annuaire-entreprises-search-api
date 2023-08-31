from aio_proxy.response.helpers import get_value
from aio_proxy.response.unite_legale_model import UniteLegaleElu


def format_elus(elus=None):
    formatted_elus = []
    if elus:
        for elu in elus:
            annee_de_naissance = (
                get_value(elu, "date_naissance")[:4]
                if get_value(elu, "date_naissance")
                else None
            )

            formatted_elu = UniteLegaleElu(
                nom=get_value(elu, "nom"),
                prenoms=get_value(elu, "prenom"),
                annee_de_naissance=annee_de_naissance,
                fonction=get_value(elu, "fonction"),
                sexe=get_value(elu, "sexe"),
            )
            formatted_elus.append(formatted_elu.dict())
    return formatted_elus
