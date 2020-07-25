#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from datetime import timedelta, datetime

from hypothesis import given, settings, Verbosity, strategies, example, Phase

import immutables

from travertine.types import Undefined, TypedAttribute, SimpleType, TypeName
from travertine.procedures import (
    UndefinedProcedure,
    ConstantProcedure,
    GetAttributeProcedure,
    SetFallbackEnvProcedure,
    SetEnvProcedure,
    VarnameProcedure,
    MapReduceProcedure,
    LoopProcedure,
    BranchingProcedure,
    BacktrackingBranchingProcedure,
)
from travertine.aggregators import (
    SumAggregator,
    MultAggregator,
    DivideAggregator,
    MaxAggregator,
    MinAggregator,
    CountAggregator,
    TakeFirstAggregator,
    TakeLastAggregator,
    AverageAggregator,
    FirstTimesCountAggregator,
    LastTimesCountAggregator,
)
from travertine.splitters import IdentitySplitter, RequestSplitter
from travertine.predicates import (
    ValidityPredicate,
    ExecutionPredicate,
    MatchesAttributePredicate,
    QuantityPredicate,
    AttributeInRangePredicate,
    Otherwise,
)

from travertine.testing.strategies.structs import (
    demands,
    commodities,
    requests,
    Demand,
    Commodity,
    Request,
)

from .tools import prices, PriceCase, NULL_DEMAND, EMPTY_ENV


DAY = timedelta(1)


class TestPriceProcedures(PriceCase):
    @given(demands(), prices)
    def test_ConstantProcedure(self, demand, price):
        "A constant procedure always returns the same price."
        procedure = ConstantProcedure(price)
        result = procedure(demand, EMPTY_ENV)
        self.assertPriceMatches(result, price)
        self.assertPriceMatches(result, procedure(demand, EMPTY_ENV))

    @given(demands())
    def test_UndefinedProcedure(self, demand):
        "The undefined procedure always returns Undefined."
        procedure = UndefinedProcedure()
        result = procedure(demand, EMPTY_ENV)
        self.assertPriceMatches(result, Undefined)
        self.assertPriceMatches(result, procedure(demand, EMPTY_ENV))

    def test_GetAttributeProcedure_undefined(self):
        procedure = GetAttributeProcedure(ATTR_PRICE)
        result = procedure(NULL_DEMAND, EMPTY_ENV)
        self.assertPriceMatches(result, Undefined)
        self.assertPriceMatches(result, procedure(NULL_DEMAND, EMPTY_ENV))

    @given(commodities(), prices, strategies.datetimes())
    def test_GetAttributeProcedure(self, commodity, price, date):
        commodity.price = price
        procedure = GetAttributeProcedure(ATTR_PRICE)
        result = procedure(Demand.from_commodities([commodity], date=date), EMPTY_ENV)
        self.assertPriceMatches(result, price)
        self.assertPriceMatches(
            result, procedure(Demand.from_commodities([commodity], date=date), EMPTY_ENV)
        )

    @given(prices, prices, prices)
    def test_variables_with_defaults(self, default, fallback_value, value):
        varproc = VarnameProcedure("value", default)
        result = varproc(NULL_DEMAND, EMPTY_ENV)
        self.assertPriceMatches(result, default)
        self.assertPriceMatches(result, varproc(NULL_DEMAND, EMPTY_ENV))

        proc = SetFallbackEnvProcedure(immutables.Map(value=fallback_value), varproc)
        result = proc(NULL_DEMAND, EMPTY_ENV)
        self.assertPriceMatches(result, fallback_value)
        self.assertPriceMatches(result, proc(NULL_DEMAND, EMPTY_ENV))

        proc = SetEnvProcedure(immutables.Map(value=value), proc)
        result = proc(NULL_DEMAND, EMPTY_ENV)
        self.assertPriceMatches(result, value)
        self.assertPriceMatches(result, proc(NULL_DEMAND, EMPTY_ENV))


ATTR_STANDARD_PRICE = TypedAttribute("standard_price", SimpleType.from_python_type(float))
GET_ATTR_STANDARD_PRICE_PROC = GetAttributeProcedure(ATTR_STANDARD_PRICE)

ATTR_PRICE = TypedAttribute("price", SimpleType.from_python_type(float))


def get_typed_attr(name, value):
    return TypedAttribute(name, SimpleType(TypeName.from_value(value)))


ATTR_MATCHING_ATTRIBUTE = lambda value: get_typed_attr("matching_attribute", value)


class TestLoop(PriceCase):
    @given(demands())
    def test_LoopProcedure_with_Sum(self, demand: Demand):
        proc = LoopProcedure(GET_ATTR_STANDARD_PRICE_PROC, SumAggregator())
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, sum(r.result for r in result.subresults))
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(demands())
    def test_LoopProcedure_with_Max(self, demand: Demand):
        proc = LoopProcedure(GET_ATTR_STANDARD_PRICE_PROC, MaxAggregator())
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, max(r.result for r in result.subresults))
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(demands())
    def test_LoopProcedure_with_Min(self, demand: Demand):
        proc = LoopProcedure(GET_ATTR_STANDARD_PRICE_PROC, MinAggregator())
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, min(r.result for r in result.subresults))
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(demands())
    def test_LoopProcedure_with_Mult(self, demand: Demand):
        import operator
        from functools import reduce

        proc = LoopProcedure(GET_ATTR_STANDARD_PRICE_PROC, MultAggregator())
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(
            result, reduce(operator.mul, (r.result for r in result.subresults), 1)
        )
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(demands(min_size=2))
    def test_LoopProcedure_with_Div(self, demand: Demand):
        proc = LoopProcedure(GET_ATTR_STANDARD_PRICE_PROC, DivideAggregator())
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(
            result, result.subresults[0].result / result.subresults[1].result
        )
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(demands())
    def test_LoopProcedure_with_Count(self, demand: Demand):
        proc = LoopProcedure(GET_ATTR_STANDARD_PRICE_PROC, CountAggregator())
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, len(result.subresults))
        self.assertPriceMatches(result, len(demand.requests))
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(demands())
    def test_LoopProcedure_with_First(self, demand: Demand):
        proc = LoopProcedure(GET_ATTR_STANDARD_PRICE_PROC, TakeFirstAggregator())
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, result.subresults[0].result)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(demands())
    def test_LoopProcedure_with_Last(self, demand: Demand):
        proc = LoopProcedure(GET_ATTR_STANDARD_PRICE_PROC, TakeLastAggregator())
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, result.subresults[-1].result)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(demands())
    def test_LoopProcedure_with_FirstCount(self, demand: Demand):
        proc = LoopProcedure(GET_ATTR_STANDARD_PRICE_PROC, FirstTimesCountAggregator())
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(
            result, result.subresults[0].result * len(result.subresults)
        )
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(demands())
    def test_LoopProcedure_with_LastCount(self, demand: Demand):
        proc = LoopProcedure(GET_ATTR_STANDARD_PRICE_PROC, LastTimesCountAggregator())
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(
            result, result.subresults[-1].result * len(result.subresults)
        )
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @settings(verbosity=Verbosity.normal)
    @given(demands())
    def test_LoopProcedure_with_Avg(self, demand: Demand):
        import statistics

        proc = LoopProcedure(GET_ATTR_STANDARD_PRICE_PROC, AverageAggregator())
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(
            result, statistics.mean([float(r.result) for r in result.subresults])
        )
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))


class TestMapReduce(PriceCase):
    @given(demands())
    def test_MapReduceProcedure(self, demand):
        proc = MapReduceProcedure(
            IdentitySplitter(), GET_ATTR_STANDARD_PRICE_PROC, SumAggregator()
        )
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, sum(r.result for r in result.subresults))
        self.assertEqual(len(result.subresults), 1)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(demands())
    def test_MapReduceProcedure_with_RequestSplitter(self, demand):
        proc = MapReduceProcedure(
            RequestSplitter(), GET_ATTR_STANDARD_PRICE_PROC, SumAggregator()
        )
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, sum(r.result for r in result.subresults))
        self.assertEqual(len(result.subresults), len(demand.requests))
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))


class TestBranches(PriceCase):
    @given(demands(), prices, prices)
    def test_ValidityPredicate(self, demand: Demand, price, default):
        date = demand.date
        start = date - DAY
        end = date + DAY
        pred = ValidityPredicate(start, end)
        proc = BranchingProcedure(
            (pred, ConstantProcedure(price)), (Otherwise(), ConstantProcedure(default))
        )
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, price)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(demands(), prices, prices)
    def test_ValidityPredicate_at_start_date(self, demand: Demand, price, default):
        date = demand.date
        start = date
        end = date + DAY
        pred = ValidityPredicate(start, end)
        proc = BranchingProcedure(
            (pred, ConstantProcedure(price)), (Otherwise(), ConstantProcedure(default))
        )
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, price)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(demands(), prices, prices)
    def test_ValidityPredicate_empty_range(self, demand: Demand, price, default):
        date = demand.date
        pred = ValidityPredicate(date, date)
        proc = BranchingProcedure(
            (pred, ConstantProcedure(price)), (Otherwise(), ConstantProcedure(default))
        )
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, default)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(demands(), prices, prices)
    def test_ValidityPredicate_off(self, demand: Demand, price, default):
        date = demand.date
        start = date - DAY
        end = date + DAY
        pred = ValidityPredicate(start, end)
        proc = BranchingProcedure(
            (pred, ConstantProcedure(price)), (Otherwise(), ConstantProcedure(default))
        )
        offdemand = demand.replace(date=start - DAY)
        result = proc(offdemand, EMPTY_ENV)
        self.assertPriceMatches(result, default)
        self.assertPriceMatches(result, proc(offdemand, EMPTY_ENV))

    @given(demands(), prices, prices)
    def test_ValidityPredicate_off_at_end_date(self, demand: Demand, price, default):
        date = demand.date
        start = date - DAY
        end = date
        pred = ValidityPredicate(start, end)
        proc = BranchingProcedure(
            (pred, ConstantProcedure(price)), (Otherwise(), ConstantProcedure(default))
        )
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, default)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(commodities(), prices, prices, strategies.datetimes())
    def test_ExecutionPredicate(self, commodity: Commodity, price, default, date):
        date = commodity.start_date
        start = date - DAY
        end = date + DAY
        pred = ExecutionPredicate(start, end)
        proc = BranchingProcedure(
            (pred, ConstantProcedure(price)), (Otherwise(), ConstantProcedure(default))
        )
        demand = Demand.from_commodities([commodity], date=date)
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, price)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

        demand = Demand.from_commodities([commodity.replace(start_date=start)], date=date)
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, price)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(commodities(), prices, prices, strategies.datetimes())
    def test_ExecutionPredicate_offseason(
        self, commodity: Commodity, price, default, date
    ):
        date = commodity.start_date
        start = date - DAY
        end = date + DAY
        pred = ExecutionPredicate(start, end)
        proc = BranchingProcedure(
            (pred, ConstantProcedure(price)), (Otherwise(), ConstantProcedure(default))
        )
        commodity = commodity.replace(start_date=start - DAY)
        demand = Demand.from_commodities([commodity], date=date)
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, default)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

        commodity = commodity.replace(start_date=end)
        demand = Demand.from_commodities([commodity], date=date)
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, default)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(commodities(), prices, prices, strategies.datetimes())
    def test_MatchesAttribute_no_match(self, commodity, price, default, date):
        pred = MatchesAttributePredicate(ATTR_MATCHING_ATTRIBUTE("yes"), "yes")
        proc = BranchingProcedure(
            (pred, ConstantProcedure(price)), (Otherwise(), ConstantProcedure(default))
        )
        demand = Demand.from_commodities([commodity], date=date)
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, default)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(commodities(), prices, prices, strategies.datetimes())
    def test_MatchesAttribute_match(self, commodity, price, default, date):
        pred = MatchesAttributePredicate(ATTR_MATCHING_ATTRIBUTE("yes"), "yes")
        proc = BranchingProcedure(
            (pred, ConstantProcedure(price)), (Otherwise(), ConstantProcedure(default))
        )
        demand = Demand.from_commodities(
            [commodity.replace(matching_attribute="yes")], date=date
        )
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, price)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(commodities(), prices, prices, strategies.datetimes())
    def test_AttributeInRange_in_range(self, commodity, price, default, date):
        pred = AttributeInRangePredicate(
            ATTR_MATCHING_ATTRIBUTE(price), price - 10, price + 10
        )
        proc = BranchingProcedure(
            (pred, ConstantProcedure(price)), (Otherwise(), ConstantProcedure(default))
        )
        demand = Demand.from_commodities(
            [commodity.replace(matching_attribute=price)], date=date
        )
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, price)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(commodities(), prices, prices, strategies.datetimes())
    def test_AttributeInRange_attribute_unset(self, commodity, price, default, date):
        pred = AttributeInRangePredicate(
            ATTR_MATCHING_ATTRIBUTE(price), price - 10, price + 10
        )
        proc = BranchingProcedure(
            (pred, ConstantProcedure(price)), (Otherwise(), ConstantProcedure(default))
        )
        demand = Demand.from_commodities([commodity], date=date)
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, default)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(commodities(), prices, prices, strategies.datetimes())
    def test_AttributeInRange_attribute_out_of_range(
        self, commodity, price, default, date
    ):
        pred = AttributeInRangePredicate(
            ATTR_MATCHING_ATTRIBUTE(price), price - 10, price + 10
        )
        proc = BranchingProcedure(
            (pred, ConstantProcedure(price)), (Otherwise(), ConstantProcedure(default))
        )
        demand = Demand.from_commodities(
            [
                # Notice that the range is open on the upper bound
                commodity.replace(matching_attribute=price + 10)
            ],
            date=date,
        )
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, default)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

        demand = Demand.from_commodities(
            [
                # Notice that the range is closed on the lower bound
                commodity.replace(matching_attribute=price - 10)
            ],
            date=date,
        )
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, price)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(requests(), prices, prices)
    def test_QuantityPredicate_no_match(self, request: Request, price, default):
        quantity = request.quantity
        upperbound = quantity + 1
        lowerbound = quantity - 1
        pred = QuantityPredicate(lowerbound, upperbound)
        proc = BranchingProcedure(
            (pred, ConstantProcedure(price)), (Otherwise(), ConstantProcedure(default))
        )
        demand = Demand.from_requests([request.replace(quantity=upperbound + 1)])
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, default)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))

    @given(requests(), prices, prices)
    def test_QuantityPredicate_match(self, request: Request, price, default):
        quantity = request.quantity
        upperbound = quantity + 1
        lowerbound = quantity - 1
        pred = QuantityPredicate(lowerbound, upperbound)
        proc = BranchingProcedure(
            (pred, ConstantProcedure(price)), (Otherwise(), ConstantProcedure(default))
        )
        demand = Demand.from_requests([request])
        result = proc(demand, EMPTY_ENV)
        self.assertPriceMatches(result, price)
        self.assertPriceMatches(result, proc(demand, EMPTY_ENV))


class TestBacktrackingBranches(PriceCase):
    @settings(phases=[Phase.explicit])
    @given(demands(min_size=1, max_size=1), prices, prices, prices)
    @example(
        Demand(
            date=datetime(2000, 1, 6, 8, 0),
            requests=(
                Request(
                    commodity=Commodity(
                        start_date=datetime(2000, 1, 6, 16, 0),
                        duration=timedelta(hours=20),
                    ),
                    quantity=1,
                ),
            ),
        ),
        69,
        69 + 69,
        69 + 69 + 69,
    )
    def test_three_tiered_backtracking_no_backtracking(
        self, demand: Demand, price, base_price, default
    ):
        date = demand.date
        start_date = demand.requests[0].commodity.start_date
        procedure = self._build_backtring_procedure(
            date, start_date, price, base_price, default
        )
        result = procedure(demand, EMPTY_ENV)
        self.assertPriceMatches(result, price)

    @settings(phases=[Phase.explicit])
    @given(demands(min_size=1, max_size=1), prices, prices, prices)
    @example(
        Demand(
            date=datetime(2000, 1, 6, 8, 0),
            requests=(
                Request(
                    commodity=Commodity(
                        start_date=datetime(2000, 1, 6, 16, 0),
                        duration=timedelta(hours=20),
                    ),
                    quantity=1,
                ),
            ),
        ),
        69,
        69 + 69,
        69 + 69 + 69,
    )
    def test_three_tiered_backtracking_perform_backtrack_in_season(
        self, demand: Demand, price, base_price, default
    ):
        date = demand.date
        start_date = demand.requests[0].commodity.start_date
        procedure = self._build_backtring_procedure(
            date, start_date, price, base_price, default
        )

        # The new demand has 'date' in the offer (and the base_offer); but the
        # commodity's start_date is not the first offer season; so we will
        # backtrack to the base_offer.
        demand = demand.replace(date=demand.date)  # just a copy
        commodity = demand.requests[0].commodity
        demand.requests[0].commodity = commodity.replace(
            start_date=commodity.start_date + 20 * DAY
        )
        result = procedure(demand, EMPTY_ENV)
        self.assertPriceMatches(result, base_price)

    @settings(phases=[Phase.explicit])
    @given(demands(min_size=1, max_size=1), prices, prices, prices)
    @example(
        Demand(
            date=datetime(2000, 1, 6, 8, 0),
            requests=(
                Request(
                    commodity=Commodity(
                        start_date=datetime(2000, 1, 6, 16, 0),
                        duration=timedelta(hours=20),
                    ),
                    quantity=1,
                ),
            ),
        ),
        69,
        69 + 69,
        69 + 69 + 69,
    )
    def test_three_tiered_backtracking_backtracking_but_nomatch(
        self, demand: Demand, price, base_price, default
    ):
        date = demand.date
        start_date = demand.requests[0].commodity.start_date
        procedure = self._build_backtring_procedure(
            date, start_date, price, base_price, default
        )

        # Finally a demand has 'date' in the offer but not the base_offer; it
        # also fails the offer's demand, so we must reach the last branch.
        demand = demand.replace(date=demand.date + 11 * DAY)
        commodity = demand.requests[0].commodity
        demand.requests[0].commodity = commodity.replace(
            start_date=commodity.start_date + 2 * DAY
        )
        result = procedure(demand, EMPTY_ENV)
        self.assertPriceMatches(result, default)

    def _build_backtring_procedure(self, date, start_date, price, base_price, default):
        # Build a chain of backtracking branching procedure with an offer and
        # base_offer built as depitected:
        #
        #                        .- demand.date           . demand's start_date
        #                        |                        |
        #                        v                        v
        #    offer          |---------------| --------> |-------| --> $price
        #
        #    base   |----------------| -----------------------------> $base_price
        #
        #    otherwise ---------------------------------------------> $default
        #
        offer = ValidityPredicate(date - 5 * DAY, date + 15 * DAY)
        base_offer = ValidityPredicate(date - 10 * DAY, date + 10 * DAY)
        season = ExecutionPredicate(start_date - DAY, start_date + DAY)
        season_procedure = BacktrackingBranchingProcedure(
            (season, ConstantProcedure(price))
        )
        procedure = BacktrackingBranchingProcedure(
            (offer, season_procedure),
            (base_offer, ConstantProcedure(base_price)),
            (Otherwise(), ConstantProcedure(default)),
        )
        return procedure

    @given(commodities())
    def test_regression_issue_869_backtracking_too_early(self, commodity):
        #  We were performing backtracking to early for predicates of kind
        #  MATCH.
        #
        # The bug only happens when the MATCH procedure is called in the
        # context of another backtracking procedure.
        match_procedure = BacktrackingBranchingProcedure(
            (
                (
                    MatchesAttributePredicate(ATTR_MATCHING_ATTRIBUTE(1), 1),
                    ConstantProcedure(42),
                )
            )
        )
        date = datetime.utcnow()
        top_procedure = BacktrackingBranchingProcedure(
            (ValidityPredicate(date - DAY, date + DAY), match_procedure)
        )
        demand = Demand.from_commodities(
            (commodity.replace(matching_attribute=1),), date=date
        )
        price = top_procedure(demand, EMPTY_ENV)
        self.assertPriceMatches(price, 42)
