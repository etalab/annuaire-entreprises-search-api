import re

import pytest
from aio_proxy.tests.e2e_tests.response_tester import APIResponseTester

min_total_results = 10
min_total_results_filters = 1000


@pytest.fixture
def api_response_tester():
    api_url = "http://localhost:4500/"
    return APIResponseTester(api_url)


def test_fetch_company(api_response_tester):
    """
    test if searching for `la poste` returns the right siren as the first search result.
    """
    path = "search?q=la poste"
    api_response_tester.test_field_value(path, "siren", "356000000")
    api_response_tester.test_number_of_results(path, min_total_results)


def test_personne_filter(api_response_tester):
    """
    test if using `personne` filters returns the right siren (ganymede)
    """
    path = (
        "search?nom_personne=jouppe&prenoms_personne=xavier erwan"
        "&date_naissance_personne_min=1970-01-01"
        "&date_naissance_personne_max"
        "=2000-01-01"
    )
    api_response_tester.test_field_value(path, "siren", "880878145")
    api_response_tester.test_number_of_results(path, 1)


def test_error_query(api_response_tester):
    """
    test if giving wrong query parameters returns an error.
    """
    path = "search?qs=ganymede"
    api_response_tester.assert_api_response_code_400(path)


def test_accept_three_characters(api_response_tester):
    """
    test if API returns results for a three character query.
    """
    path = "search?q=abc"
    api_response_tester.assert_api_response_code_200(path)


def test_format_date_naissance(api_response_tester):
    """
    test if using the wrong date of birth returns an error.
    """
    path = "search?date_naissance_personne_min=13/09/2001"
    api_response_tester.assert_api_response_code_400(path)


def test_query_too_short(api_response_tester):
    """
    test if API returns an error for a two character query
    """
    path = "search?q=ab"
    api_response_tester.assert_api_response_code_400(path)


def test_short_query_with_filter(api_response_tester):
    """
    test if using a filter with a two character query returns results.
    """
    path = "search?q=ab&code_postal=75015"
    api_response_tester.assert_api_response_code_200(path)


def test_terms_empty_only(api_response_tester):
    """
    test if searching using empty search parameters returns an error.
    """
    path = "search?q="
    api_response_tester.assert_api_response_code_400(path)


def test_bool_filters(api_response_tester):
    """
    test if using "est_rge" and "convention_collective_renseignee" filters returns only
    établissements` with `rge` and `convention collective` ids.
    """
    path = "search?convention_collective_renseignee=true&est_rge=true"
    api_response_tester.test_number_of_results(path, 1)
    api_response_tester.test_field_value(path, "complements.est_rge", True)


def test_organisme_formation(api_response_tester):
    """
    test est_organisme_formation et est_qualiopi
    """
    path = "search?est_organisme_formation=true&est_qualiopi=true"
    api_response_tester.test_number_of_results(path, min_total_results_filters)


def test_near_point(api_response_tester):
    """
    test near point endpoint
    """
    path = "near_point?lat=48&long=2&radius=5"
    api_response_tester.assert_api_response_code_200(path)


def test_categorie_entreprise_list(api_response_tester):
    """
    test categorie_entreprise filter
    """
    path = "search?categorie_entreprise=GE,PME"
    api_response_tester.assert_api_response_code_200(path)


def test_banned_param(api_response_tester):
    """
    test if banned param returns a 400 status code.
    """
    path = "search?localisation=45000"
    api_response_tester.assert_api_response_code_400(path)


def test_siren_search(api_response_tester):
    """
    test if valid `siren` search returns results
    """
    path = "search?q=130025265"
    api_response_tester.assert_api_response_code_200(path)
    api_response_tester.test_field_value(path, "siren", "130025265")


def test_siret_search(api_response_tester):
    """
    test if valid `siret` search returns results
    """
    path = "search?q=88087814500015"
    response = api_response_tester.get_api_response(path)
    api_response_tester.assert_api_response_code_200(path)
    api_response_tester.test_field_value(path, "siren", "880878145")
    assert response.json()["total_results"] == 1
    assert (
        response.json()["results"][0]["matching_etablissements"][0]["siret"]
        == "88087814500015"
    )


def test_page_number(api_response_tester):
    """
    test if giving a page number higher than 1000 returns a value error
    """
    path = "search?q=ganymede&page=10001"
    api_response_tester.assert_api_response_code_400(path)


def test_min_per_page(api_response_tester):
    """
    test if giving a per_page smaller than 0, return a value error
    """
    path = "search?q=ganymede&per_page=0"
    api_response_tester.assert_api_response_code_400(path)


def test_est_service_public(api_response_tester):
    """
    test if `est_service_public`  filter returns results with and without text search.
    """
    path = "search?est_service_public=true"
    api_response_tester.test_number_of_results(path, min_total_results_filters)
    api_response_tester.test_field_value(path, "complements.est_service_public", True)
    path = "search?est_service_public=true&q=ministere"
    api_response_tester.test_field_value(path, "complements.est_service_public", True)


def test_est_societe_a_mission(api_response_tester):
    """
    test est_societe_mission
    """
    path = "search?est_societe_mission=true"
    api_response_tester.test_number_of_results(path, 500)
    api_response_tester.test_field_value(path, "complements.est_societe_mission", True)


def test_commune_filter(api_response_tester):
    path = "search?code_commune=35235"
    api_response_tester.test_field_value(
        path, "matching_etablissements.0.commune", "35235"
    )


def test_activite_principale_filter(api_response_tester):
    path = "search?activite_principale=01.12Z"
    api_response_tester.test_field_value(path, "activite_principale", "01.12Z")


def test_categorie_entreprise(api_response_tester):
    path = "search?categorie_entreprise=PME"
    api_response_tester.test_field_value(path, "categorie_entreprise", "PME")


def test_code_collectivite_territoriale(api_response_tester):
    path = "search?code_collectivite_territoriale=75C"
    api_response_tester.test_field_value(
        path, "complements.collectivite_territoriale.code", "75C"
    )


def test_convention_collective_renseignee(api_response_tester):
    path = "search?convention_collective_renseignee=true"
    api_response_tester.test_field_value(
        path, "complements.convention_collective_renseignee", True
    )


def test_departement(api_response_tester):
    path = "search?departement=10"
    response = api_response_tester.get_api_response(path)
    commune = response.json()["results"][0]["matching_etablissements"][0]["commune"]
    assert re.match(r"^10\w{3}$", commune) is not None


def test_egapro_renseignee(api_response_tester):
    path = "search?egapro_renseignee=true"
    api_response_tester.test_field_value(path, "complements.egapro_renseignee", True)


def test_est_association(api_response_tester):
    path = "search?est_association=True"
    response = api_response_tester.get_api_response(path)
    id_asso = response.json()["results"][0]["complements"]["identifiant_association"]
    assert id_asso is not None


def test_est_collectivite_territoriale(api_response_tester):
    path = "search?est_collectivite_territoriale=true"
    response = api_response_tester.get_api_response(path)
    coll_terr = response.json()["results"][0]["complements"][
        "collectivite_territoriale"
    ]
    assert coll_terr is not None


def test_est_bio(api_response_tester):
    path = "search?est_bio=true"
    api_response_tester.test_field_value(path, "complements.est_bio", True)


def test_est_entrepreneur_individuel(api_response_tester):
    path = "search?est_entrepreneur_individuel=true"
    api_response_tester.test_field_value(
        path, "complements.est_entrepreneur_individuel", True
    )


def test_est_entrepreneur_spectacle(api_response_tester):
    path = "search?est_entrepreneur_spectacle=true"
    api_response_tester.test_field_value(
        path, "complements.est_entrepreneur_spectacle", True
    )


def test_est_rge(api_response_tester):
    path = "search?est_rge=true"
    api_response_tester.test_field_value(path, "complements.est_rge", True)


def test_est_finess(api_response_tester):
    path = "search?est_finess=true"
    api_response_tester.test_field_value(path, "complements.est_finess", True)


def test_est_ess(api_response_tester):
    path = "search?est_ess=true"
    api_response_tester.test_field_value(path, "complements.est_ess", True)


def test_est_organisme_formation(api_response_tester):
    path = "search?est_organisme_formation=true"
    api_response_tester.test_field_value(
        path, "complements.est_organisme_formation", True
    )


def test_est_qualiopi(api_response_tester):
    path = "search?est_qualiopi=true"
    api_response_tester.test_field_value(path, "complements.est_qualiopi", True)


def test_est_uai(api_response_tester):
    path = "search?est_uai=true"
    api_response_tester.test_field_value(path, "complements.est_uai", True)


def test_etat_administratif(api_response_tester):
    path = "search?etat_administratif=C"
    api_response_tester.test_field_value(path, "etat_administratif", "C")


def test_id_convention_collective(api_response_tester):
    path = "search?id_convention_collective=1090"
    response = api_response_tester.get_api_response(path)
    liste_idcc = response.json()["results"][0]["matching_etablissements"][0][
        "liste_idcc"
    ]
    assert "1090" in liste_idcc


def test_id_finess(api_response_tester):
    path = "search?id_finess=010003853"
    response = api_response_tester.get_api_response(path)
    liste_finess = response.json()["results"][0]["matching_etablissements"][0][
        "liste_finess"
    ]
    assert "010003853" in liste_finess


def test_id_rge(api_response_tester):
    path = "search?id_rge=8611M10D109"
    response = api_response_tester.get_api_response(path)
    liste_rge = response.json()["results"][0]["matching_etablissements"][0]["liste_rge"]
    assert "8611M10D109" in liste_rge


def test_id_uai(api_response_tester):
    path = "search?id_uai=0022004T"
    response = api_response_tester.get_api_response(path)
    liste_uai = response.json()["results"][0]["matching_etablissements"][0]["liste_uai"]
    assert "0022004T" in liste_uai


def test_nature_juridique(api_response_tester):
    path = "search?nature_juridique=7344"
    api_response_tester.test_field_value(path, "nature_juridique", "7344")


def test_section_activite_principale(api_response_tester):
    path = "search?section_activite_principale=A"
    api_response_tester.test_field_value(path, "section_activite_principale", "A")


def test_tranche_effectif_salarie(api_response_tester):
    path = "search?tranche_effectif_salarie=01"
    api_response_tester.test_field_value(path, "tranche_effectif_salarie", "01")


def test_date_naiss_interval(api_response_tester):
    path = (
        "search?date_naissance_personne_min="
        "1990-01-01&date_naissance_personne_max=1989-01-01"
    )
    api_response_tester.assert_api_response_code_400(path)


def test_type_personne(api_response_tester):
    path = "search?type_personne=elu&nom_personne=xavier"
    response = api_response_tester.get_api_response(path)
    elus = response.json()["results"][0]["complements"]["collectivite_territoriale"][
        "elus"
    ]
    assert elus is not None


def test_selected_fields(api_response_tester):
    path = (
        "search?q=ganymede&minimal=True&include=siege,dirigeants"
        "&include_admin=etablissements"
    )
    response = api_response_tester.get_api_response(path)
    etablissements = response.json()["results"][0]["etablissements"]
    assert etablissements
    assert "siege" in response.json()["results"][0]
    assert "dirigeants" in response.json()["results"][0]
    assert "score" not in response.json()["results"][0]
    assert "complements" not in response.json()["results"][0]


def test_minimal_response(api_response_tester):
    path = "search?q=ganymede&minimal=True"
    response = api_response_tester.get_api_response(path)
    assert "siege" not in response.json()["results"][0]
    assert "dirigeants" not in response.json()["results"][0]
    assert "score" not in response.json()["results"][0]
    assert "complements" not in response.json()["results"][0]
    assert "matching_etablissements" not in response.json()["results"][0]


def test_minimal_fail(api_response_tester):
    path = "search?q=ganymede&include=siege"
    api_response_tester.assert_api_response_code_400(path)


def test_region_filter(api_response_tester):
    path = "search?region=76"
    response = api_response_tester.get_api_response(path)
    region_etablissement = response.json()["results"][0]["matching_etablissements"][0][
        "region"
    ]
    assert region_etablissement == "76"


def test_non_diffusibilite(api_response_tester):
    path = "search?q=300210820&include_admin=etablissements"
    response = api_response_tester.get_api_response(path)
    assert response.json()["results"][0]["nom_complet"] == "[NON-DIFFUSIBLE]"
    assert response.json()["results"][0]["siege"]["code_postal"] == "[NON-DIFFUSIBLE]"
    for etablissement in response.json()["results"][0]["etablissements"]:
        assert etablissement["code_postal"] == "[NON-DIFFUSIBLE]"
    for dirigeant in response.json()["results"][0]["dirigeants"]:
        assert dirigeant["prenoms"] == "[NON-DIFFUSIBLE]"
        assert dirigeant["nom"] == "[NON-DIFFUSIBLE]"
