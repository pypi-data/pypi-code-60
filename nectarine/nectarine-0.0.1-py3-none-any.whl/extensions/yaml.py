"""
Module providing a ConfigurationProvider backed by a YAML file
"""

import yaml as pyyaml

from nectarine.providers.dictionary import Dictionary


class Yaml(Dictionary):
    def __init__(self, file: str):
        with open(file, 'r') as f:
            value = pyyaml.safe_load(f)
        super().__init__(value)


def yaml(file: str):
    return lambda: Yaml(file)
