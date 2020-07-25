#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import unittest
from functools import partial

import immutables
from hypothesis import strategies

from travertine.types import Environment, Undefined, PriceResultType
from travertine.structs import Demand, PriceResult


prices = strategies.integers(min_value=1, max_value=10 ** 12)
maybe_prices = prices | strategies.just(Undefined)


class PriceCaseMixin:
    def assertPriceMatches(self, result, expected, places=None, only_result=True):
        if places is None:
            assertFn = self.assertEqual
        else:
            assertFn = partial(self.assertAlmostEqual, places=places)

        if isinstance(expected, PriceResult):
            assertFn(result.result, expected.result)
        else:
            assertFn(result.result, expected)


class PriceCase(unittest.TestCase, PriceCaseMixin):
    pass


class KaboomProcedure:
    def __call__(self, demand: Demand, env: Environment) -> PriceResultType:
        raise AssertionError("Should have been called")

    @property
    def avm(self):
        return {}


EMPTY_ENV: Environment = immutables.Map()
NULL_DEMAND = Demand(None, ())  # type: ignore
