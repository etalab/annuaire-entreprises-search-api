def hide_non_diffusible_fields(result_formatted):
    hidden_fields = [
        "nom_complet",
        "nom_raison_sociale",
        "sigle",
    ]
    for field in result_formatted.keys():
        if field in hidden_fields:
            result_formatted[field] = "[NON-DIFFUSIBLE]"

        if field == "siege":
            result_formatted["siege"] = hide_non_diffusible_etablissement_fields(
                result_formatted["siege"]
            )

        if field == "dirigeants":
            result_formatted["dirigeants"] = hide_non_diffusible_dirirgeants_fields(
                result_formatted["dirigeants"]
            )

        if field == "matching_etablissements":
            for matching_etablissement in result_formatted["matching_etablissements"]:
                matching_etablissement = hide_non_diffusible_etablissement_fields(
                    matching_etablissement
                )

        if field == "etablissements":
            for etablissement in result_formatted["etablissements"]:
                etablissement = hide_non_diffusible_etablissement_fields(etablissement)

    return result_formatted


def hide_non_diffusible_dirirgeants_fields(dirigeants):
    for dirigeant in dirigeants:
        if dirigeant["type_dirigeant"] == "personne physique":
            dirigeant["nom"] = "[NON-DIFFUSIBLE]"
            dirigeant["prenoms"] = "[NON-DIFFUSIBLE]"
            dirigeant["annee_de_naissance"] = "[NON-DIFFUSIBLE]"
    return dirigeants


def hide_non_diffusible_etablissement_fields(etablissement):
    # in order to keep `liste_enseignes` as an array of "NON-DIFFUSIBLE" strings
    if etablissement["liste_enseignes"]:
        etablissement["liste_enseignes"] = [
            "[NON-DIFFUSIBLE]" for enseigne in etablissement["liste_enseignes"]
        ]
    non_diffusible_fields = [
        "cedex",
        "code_postal",
        "complement_adresse",
        "distribution_speciale",
        "indice_repetition",
        "libelle_cedex",
        "libelle_voie",
        "nom_commercial",
        "numero_voie",
        "type_voie",
    ]
    for field in non_diffusible_fields:
        etablissement[field] = "[NON-DIFFUSIBLE]"
    return etablissement
