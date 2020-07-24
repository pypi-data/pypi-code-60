# -*- coding: utf-8 -*-
from typing import Iterable, ClassVar

from .actions import CopyAction
from .schema import CopySchema
from ..feature import Feature
from ..schema import FeatureSchema
from ...action import Action


class CopyFeature(Feature):
    """
    Copy files from local filesystem or URL to one of many directories.
    """

    @property
    def name(self) -> str:
        return "copy"

    @property
    def schema(self) -> ClassVar[FeatureSchema]:
        return CopySchema

    @property
    def actions(self) -> Iterable[Action]:
        return (
            CopyAction(),
        )
