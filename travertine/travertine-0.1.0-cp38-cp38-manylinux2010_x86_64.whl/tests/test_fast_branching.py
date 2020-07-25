#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import pickle
import unittest

from hypothesis import strategies as st, given, settings
from hypothesis.stateful import rule, run_state_machine_as_test

from travertine.structs import EMPTY_ENV
from travertine.procedures import BranchingProcedure, ConstantProcedure
from travertine.predicates import MatchesAttributePredicate

from travertine.testing.strategies.programs import ProcedureMachine
from travertine.testing.strategies.structs import Demand, Commodity, demands

from .tools import PriceCaseMixin
from .test_pricing_models import ATTR_MATCHING_ATTRIBUTE


class BranchingMachine(ProcedureMachine, PriceCaseMixin):
    @rule(procedure=ProcedureMachine.branching_procedures, demand=demands())
    def check_look_tables_are_unpickled(self, procedure, demand):
        match_table = procedure.match_table
        interval_tree = procedure.interval_tree
        procedure = pickle.loads(pickle.dumps(procedure))
        self.assertEqual(match_table, procedure.match_table)
        self.assertEqual(interval_tree, procedure.interval_tree)


class ProgramCase(unittest.TestCase, PriceCaseMixin):
    maxDiff = None

    def test_all_programs_compute_the_same(self):
        class _ProgramMachine(BranchingMachine):
            assertEqual = self.assertEqual
            assertAlmostEqual = self.assertAlmostEqual

        run_state_machine_as_test(_ProgramMachine)

    @settings(deadline=None)
    @given(
        st.integers(min_value=100, max_value=1000).flatmap(
            lambda last: st.tuples(
                st.just(last), st.integers(min_value=0, max_value=last)
            )
        )
    )
    def test_well_typed_MatchesAttribute_gets_attribute_only_once(self, args):
        last, picked = args

        hits = 0
        matching_value = "value-%d" % picked
        matching_attribute = ATTR_MATCHING_ATTRIBUTE(matching_value)

        class CountedCommodity(Commodity):
            def __getattr__(self, attr):
                if attr == matching_attribute.name:
                    nonlocal hits
                    hits += 1
                    return matching_value
                else:
                    raise AttributeError(attr)

        branches = [
            (
                MatchesAttributePredicate(matching_attribute, "value-%d" % i),
                ConstantProcedure(i),
            )
            for i in range(last + 1)
        ]
        proc = BranchingProcedure(*branches)
        self.assertEqual(len(proc.match_table), last + 1)
        demand = Demand.from_commodities([CountedCommodity(None, None)])
        result = proc(demand, EMPTY_ENV)
        self.assertEqual(hits, 1)
        self.assertPriceMatches(result, picked)
