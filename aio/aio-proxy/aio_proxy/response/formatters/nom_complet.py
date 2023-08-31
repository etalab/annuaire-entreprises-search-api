def format_nom_complet(
    nom_complet,
    sigle=None,
    denomination_usuelle_1=None,
    denomination_usuelle_2=None,
    denomination_usuelle_3=None,
):
    """Add `denomination usuelle` fields and `sigle` to `nom_complet`."""
    all_denomination_usuelle = ""
    for item in [
        denomination_usuelle_1,
        denomination_usuelle_2,
        denomination_usuelle_3,
    ]:
        if item:
            all_denomination_usuelle += f"{item} "
    if all_denomination_usuelle:
        nom_complet = f"{nom_complet} ({all_denomination_usuelle.strip()})"
    if sigle:
        nom_complet = f"{nom_complet} ({sigle})"
    if nom_complet:
        return nom_complet.upper()
    # if nom_complet is null
    return None
