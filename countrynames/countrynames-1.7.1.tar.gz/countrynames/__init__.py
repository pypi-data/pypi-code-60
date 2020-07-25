import os
import yaml
import logging
import Levenshtein
from normality import normalize
from functools import lru_cache

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from .mappings import mappings

log = logging.getLogger(__name__)

__all__ = ["to_code", "to_code_3"]

COUNTRY_NAMES = {}


def _normalize_name(country):
    """Clean up a country name before comparison."""
    return normalize(country, latinize=True)


def _load_data():
    """Load known aliases from a YAML file. Internal."""
    data_file = os.path.join(os.path.dirname(__file__), "data.yaml")
    with open(data_file, "r", encoding="utf-8") as fh:
        for code, names in yaml.load(fh, Loader=Loader).items():
            code = code.strip().upper()
            COUNTRY_NAMES[_normalize_name(code)] = code
            for name in names:
                COUNTRY_NAMES[_normalize_name(name)] = code


def _fuzzy_search(name):
    best_code = None
    best_distance = None
    for cand, code in COUNTRY_NAMES.items():
        if len(cand) <= 4:
            continue
        distance = Levenshtein.distance(name, cand)
        if best_distance is None or distance < best_distance:
            best_distance = distance
            best_code = code
    if best_distance > (len(name) * 0.15):
        return None
    log.debug("Guessing country: %s -> %s (distance %d)", name, code, best_distance)
    return best_code


@lru_cache(maxsize=5000)
def to_code(country_name, fuzzy=False):
    """Given a human name for a country, return a two letter code.

    Arguments:
        ``fuzzy``: Try fuzzy matching based on Levenshtein distance.
    """
    # Lazy load country list
    if not len(COUNTRY_NAMES):
        _load_data()

    # shortcut before costly ICU stuff
    if isinstance(country_name, str):
        country_name = country_name.upper().strip()
        # Check if the input is actually an ISO code:
        if country_name in COUNTRY_NAMES.values():
            return country_name

    # Transliterate and clean up
    name = _normalize_name(country_name)
    if name is None:
        return

    # Direct look up
    code = COUNTRY_NAMES.get(name)
    if code == "FAIL":
        return None

    # Find closest match with spelling mistakes
    if code is None and fuzzy is True:
        code = _fuzzy_search(name)
    return code


def to_code_3(country_name, fuzzy=False):
    """Given a human name for a country, return a three letter code.

    Arguments:
        ``fuzzy``: Try fuzzy matching based on Levenshtein distance.
    """
    code = to_code(country_name, fuzzy=fuzzy)
    if code and len(code) > 2:
        return code
    elif code is None:
        return code
    else:
        return mappings[code]
