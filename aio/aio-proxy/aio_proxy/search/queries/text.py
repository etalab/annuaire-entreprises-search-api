def build_text_query(terms: str, matching_size: int):
    min_etab_ouverts_multiplier = {
        "field": "nombre_etablissements_ouverts",
        "factor": 1,
        "modifier": "log2p",
        "missing": 1,
    }
    mid_etab_ouverts_multiplier = {
        "field": "nombre_etablissements_ouverts",
        "factor": 10,
        "modifier": "log2p",
        "missing": 1,
    }
    max_etab_ouverts_multiplier = {
        "field": "nombre_etablissements_ouverts",
        "factor": 1000,
        "modifier": "log2p",
        "missing": 1,
    }

    text_query = {
        "bool": {
            "should": [
                {
                    "function_score": {
                        "query": {
                            "match_phrase": {
                                "unite_legale.identifiant_association_unite_legale": {
                                    "query": terms,
                                    "boost": 50,
                                    "_name": "exact match id association sirene",
                                }
                            }
                        },
                        "field_value_factor": mid_etab_ouverts_multiplier,
                    }
                },
                {
                    "match_phrase": {
                        "association.identifiant_association": {
                            "query": terms,
                            "boost": 50,
                            "_name": "exact match id association rna",
                        }
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match_phrase": {
                                "nom_complet.keyword": {
                                    "query": terms,
                                    "boost": 300,
                                    "_name": "exact nom_complet match",
                                }
                            }
                        },
                        "field_value_factor": max_etab_ouverts_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match": {
                                "nom_complet": {
                                    "query": terms,
                                    "operator": "AND",
                                    "boost": 50,
                                    "_name": "partial nom_complet match with AND",
                                }
                            }
                        },
                        "field_value_factor": mid_etab_ouverts_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match_phrase": {
                                "unite_legale.sigle.keyword": {
                                    "query": terms,
                                    "boost": 100,
                                    "_name": "exact sigle match",
                                }
                            }
                        },
                        "field_value_factor": max_etab_ouverts_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "multi_match": {
                                "query": terms,
                                "fields": [
                                    "unite_legale.nom_raison_sociale",
                                    "unite_legale.denomination_usuelle_1_unite_legale",
                                    "unite_legale.denomination_usuelle_2_unite_legale",
                                    "unite_legale.denomination_usuelle_3_unite_legale",
                                    "unite_legale.sigle",
                                    "unite_legale.nom",
                                    "unite_legale.prenom",
                                ],
                                "type": "cross_fields",
                                "operator": "AND",
                                "_name": "match all champs denomination",
                            }
                        },
                        "field_value_factor": mid_etab_ouverts_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "nested": {
                                "path": "unite_legale.etablissements",
                                "query": {
                                    "bool": {
                                        "should": [
                                            {
                                                "match_phrase": {
                                                    "unite_legale.etablissements."
                                                    "enseigne_1.keyword": {
                                                        "query": terms,
                                                        "boost": 25,
                                                        "_name": "exact match "
                                                        "enseigne 1",
                                                    }
                                                }
                                            },
                                            {
                                                "match": {
                                                    "unite_legale.\
                                                     etablissements.enseigne_1": {
                                                        "query": terms,
                                                        "operator": "AND",
                                                        "boost": 10,
                                                        "_name": "partial match "
                                                        "enseigne 1",
                                                    }
                                                }
                                            },
                                            {
                                                "match_phrase": {
                                                    "unite_legale.etablissements."
                                                    "enseigne_2.keyword": {
                                                        "query": terms,
                                                        "boost": 25,
                                                        "_name": "exact match "
                                                        "enseigne 2",
                                                    }
                                                }
                                            },
                                            {
                                                "match": {
                                                    "unite_legale.etablissements.\
                                                        enseigne_2": {
                                                        "query": terms,
                                                        "operator": "AND",
                                                        "boost": 10,
                                                        "_name": "partial match "
                                                        "enseigne 2",
                                                    }
                                                }
                                            },
                                            {
                                                "match_phrase": {
                                                    "unite_legale.etablissements.enseigne_3."
                                                    "keyword": {
                                                        "query": terms,
                                                        "boost": 25,
                                                        "_name": "exact "
                                                        "match enseigne 3",
                                                    }
                                                }
                                            },
                                            {
                                                "match": {
                                                    "unite_legale.etablissements.\
                                                        enseigne_3": {
                                                        "query": terms,
                                                        "operator": "AND",
                                                        "boost": 10,
                                                        "_name": "partial match "
                                                        "enseigne 3",
                                                    }
                                                }
                                            },
                                            {
                                                "match": {
                                                    "unite_legale.etablissements.\
                                                        adresse": {
                                                        "query": terms,
                                                        "operator": "AND",
                                                        "_name": "partial match "
                                                        "adresse",
                                                    }
                                                }
                                            },
                                            {
                                                "match": {
                                                    "unite_legale.etablissements.\
                                                        nom_commercial": {
                                                        "query": terms,
                                                        "operator": "AND",
                                                        "boost": 10,
                                                        "_name": "partial match "
                                                        "nom commercial",
                                                    }
                                                }
                                            },
                                            {
                                                "multi_match": {
                                                    "query": terms,
                                                    "fields": [
                                                        "unite_legale.etablissements.nom_complet^15",
                                                        "unite_legale.etablissements.enseigne_1",
                                                        "unite_legale.etablissements.enseigne_2",
                                                        "unite_legale.etablissements.enseigne_3",
                                                        "unite_legale.etablissements.nom_commercial",
                                                        "unite_legale.etablissements.adresse",
                                                        "unite_legale.etablissements.commune",
                                                        "unite_legale.etablissements.concat_"
                                                        "unite_legale.enseigne_adresse_siren_siret",
                                                    ],
                                                    "type": "cross_fields",
                                                    "operator": "AND",
                                                    "_name": "match nom complet et "
                                                    "adresse",
                                                }
                                            },
                                        ],
                                    }
                                },
                                "inner_hits": {
                                    "size": matching_size,
                                    "sort": {
                                        "unite_legale.etablissements."
                                        "etat_administratif": {"order": "asc"}
                                    },
                                },
                            }
                        },
                        "field_value_factor": min_etab_ouverts_multiplier,
                        "min_score": 4,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match": {
                                "unite_legale.liste_dirigeants": {
                                    "query": terms,
                                    "operator": "AND",
                                    "boost": 10,
                                    "_name": "partial match liste dirigeants",
                                }
                            }
                        },
                        "field_value_factor": mid_etab_ouverts_multiplier,
                    }
                },
                {
                    "function_score": {
                        "query": {
                            "match": {
                                "unite_legale.liste_elus": {
                                    "query": terms,
                                    "operator": "AND",
                                    "boost": 10,
                                    "_name": "partial match liste élus",
                                }
                            }
                        },
                        "field_value_factor": mid_etab_ouverts_multiplier,
                    }
                },
            ],
        }
    }
    return text_query
