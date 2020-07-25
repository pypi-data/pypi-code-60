#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import unittest
from collections.abc import Mapping
from datetime import datetime as d, datetime

from xotless.domains import Range, IntervalSet

from hypothesis.stateful import rule

from travertine.types import AttributeLocator
from travertine.predicates import (
    ValidityPredicate,
    QuantityPredicate,
    Otherwise,
    MatchesAttributePredicate,
)
from travertine.procedures import (
    ConstantProcedure,
    BranchingProcedure,
    BacktrackingBranchingProcedure,
)
from travertine.avm import MergedAVM, CascadingAVM, FilteringAVM

from travertine.testing.strategies.programs import ProcedureMachine, QUANTITY_ATTR


class AVMMachine(ProcedureMachine):
    @rule(proc=ProcedureMachine.procedures)
    def check_programs_can_compute_avms(self, proc):
        assert isinstance(proc.avm, Mapping)

    @rule(proc=ProcedureMachine.basic_procedures)
    def check_basic_procs_have_empty_avms(self, proc):
        assert not list(proc.avm.items())

    @rule(proc=ProcedureMachine.branching_procedures)
    def check_branching_procs_have_non_empty_avms(self, proc):
        assert list(
            proc.avm.items()
        ), f"Branching procedure {proc} does not have a non empty AVM: {proc.avm}"

    @rule(proc=ProcedureMachine.validity_branching_procedures)
    def check_validity_checks_demands_date_avms(self, proc):
        assert AttributeLocator.of_demand("date", datetime) in proc.avm

    @rule(proc=ProcedureMachine.quantity_branching_procedures)
    def check_quantity_checks_requests_qty_avms(self, proc):
        assert AttributeLocator.of_request("quantity", float) in proc.avm

    @rule(proc=ProcedureMachine.execution_branching_procedures)
    def check_execution_checks_commodity_startdate_avms(self, proc):
        assert AttributeLocator.of_commodity("start_date", datetime) in proc.avm


AVMMachineCase = AVMMachine.TestCase


class DomainCaseMixin:
    def assertEmpty(self, x, msg=None):
        if x:
            raise self.failureException(msg or f"{x} is not empty")

    def assertNonEmpty(self, x, msg=None):
        if not x:
            raise self.failureException(msg or f"{x} is empty")

    def assertOverlap(self, a, b, msg=None):
        r = a & b
        if not r:
            raise self.failureException(msg or f"{a} and {b} don't overlap")

    def assertDisjoint(self, a, b, msg=None):
        r = a & b
        if r:
            raise self.failureException(msg or f"{a} and {b} are not disjoint")


class AVMCase(unittest.TestCase, DomainCaseMixin):
    maxDiff = None

    def _build_scenerario(self, BranchType):
        assert BranchType in (BranchingProcedure, BacktrackingBranchingProcedure)
        return BranchType(
            # Prices from 2019-01-01 up to 2019-04-30
            (ValidityPredicate(d(2019, 1, 1), d(2019, 5, 1)), ConstantProcedure(1)),
            # Prices from 2018-12-01 up to 2019-05-31
            (ValidityPredicate(d(2018, 12, 1), d(2019, 6, 1)), ConstantProcedure(2)),
            # Prices from 2019-02-01 up to 2019-03-31; this branch is completely hidden
            # by the previous branches.
            (ValidityPredicate(d(2019, 2, 1), d(2019, 4, 1)), ConstantProcedure(3)),
            # Prices from 2019-02-01 up to 2019-06-30
            (ValidityPredicate(d(2019, 2, 1), d(2019, 7, 1)), ConstantProcedure(4)),
            # Other dates.
            (Otherwise(), ConstantProcedure(5)),
        )

    def test_branching_scenario_with_overlapping_ranges(self):
        who = self._build_scenerario(BranchingProcedure)
        date_locator = AttributeLocator.of_demand("date", datetime)
        periods = list(who.avm[date_locator])
        expected = [
            IntervalSet([Range.new_open_right(d(2019, 1, 1), d(2019, 5, 1))]),
            IntervalSet(
                [
                    Range.new_open_right(d(2018, 12, 1), d(2019, 1, 1)),
                    Range.new_open_right(d(2019, 5, 1), d(2019, 6, 1)),
                ]
            ),
            IntervalSet([Range.new_open_right(d(2019, 6, 1), d(2019, 7, 1))]),
        ]
        self.assertEqual(periods, expected)

    def test_regression_combined_avm_had_any_attribute(self):
        attr1 = AttributeLocator.of_commodity("pax_count", int)
        attr2 = AttributeLocator.of_commodity("code", str)
        attr3 = AttributeLocator.of_commodity("name", str)
        avm1 = {attr1: []}
        avm2 = {attr2: []}
        self.assertNotIn(attr3, MergedAVM(avm1, avm2))
        self.assertNotIn(attr3, FilteringAVM(avm1, avm2))
        self.assertNotIn(attr3, CascadingAVM(avm1, avm2))

    def test_branching_with_empty_AMV(self):
        v1 = ConstantProcedure(69)
        v2 = BranchingProcedure(
            (QuantityPredicate(0, 10), v1), (QuantityPredicate(10, 20), v1)
        )
        empty = BranchingProcedure((QuantityPredicate(0, 0), v2))
        nonempty = BranchingProcedure((QuantityPredicate(5, 15), v2))
        self.assertEmpty(empty.avm[QUANTITY_ATTR])
        self.assertNonEmpty(nonempty.avm[QUANTITY_ATTR])

    def test_regression_issue933_keyerror_while_iterating_over_FilteringAVM(self):
        code_locator = AttributeLocator.of_commodity("code", str)
        code_attr = code_locator.attr
        v1 = BranchingProcedure(
            (MatchesAttributePredicate(code_attr, "X"), ConstantProcedure(42))
        )
        v4 = BranchingProcedure((MatchesAttributePredicate(code_attr, "Y"), v1))
        # Notes on #933 (https://gitlab.merchise.org/mercurio-2018/xhg2/issues/933)
        #
        # Even though at this point, all the values of 'code' as been filtered
        # out, asking for the AVM's point doesn't produce the KeyError.  But
        # wrapping the AVM in another FilteringAVM for a different attribute
        # does a produce a faulty AVM.
        list(v4.avm.items())
        proc = BranchingProcedure((QuantityPredicate(-10, 100), v4))
        list(proc.avm.items())
