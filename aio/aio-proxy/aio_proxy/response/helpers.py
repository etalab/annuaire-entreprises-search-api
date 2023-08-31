import json
import os
from hashlib import sha256

from dotenv import load_dotenv

load_dotenv()

APM_URL = os.getenv("APM_URL")

CURRENT_ENV = os.getenv("ENV")

COLOR_URL = os.getenv("COLOR_URL")


def is_dev_env():
    return CURRENT_ENV == "dev"


def serialize_error_text(text: str) -> str:
    """Serialize a text string to a JSON formatted string."""
    message = {"erreur": text}
    return json.dumps(message)


def get_value(dict, key, default=None):
    """Set value to value of key if key found in dict, otherwise set value to
    default."""
    value = dict[key] if key in dict else default
    return value


def hash_string(string: str):
    hashed_string = sha256(string.encode("utf-8")).hexdigest()
    return hashed_string


def create_fields_to_include(search_params):
    if search_params.minimal:
        if search_params.include is None:
            return []
        else:
            return search_params.include
    else:
        return [
            "SIEGE",
            "FINANCES",
            "COMPLEMENTS",
            "DIRIGEANTS",
            "MATCHING_ETABLISSEMENTS",
        ]


def create_admin_fields_to_include(search_params):
    if search_params.include_admin is None:
        return []
    else:
        return search_params.include_admin
