"""
Module providing a ConfigurationProvider backed by a JSON file
"""

import json

from nectarine.providers.dictionary import Dictionary


class Json(Dictionary):
    def __init__(self, file: str):
        with open(file, 'r') as f:
            value = json.load(f)
        super().__init__(value)
