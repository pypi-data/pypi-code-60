#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from hypothesis import given
from hypothesis.strategies import integers

from travertine.procedures import ConstantProcedure, FormulaProcedure
from travertine.meta import MemoizedType

from .tools import PriceCase, NULL_DEMAND, EMPTY_ENV


class Counter(metaclass=MemoizedType):
    def __init__(self, base):
        self.call_counts = 0
        self.base = base

    def __call__(self, *args):
        self.call_counts += 1
        return self.base(*args)

    def __eq__(self, other):
        if isinstance(other, Counter):
            return self.base == other.base
        else:
            return NotImplemented

    def __hash__(self):
        return hash((Counter, hash(self.base)))


class TestMemoization(PriceCase):
    def test_calling_twice_doesnt_share(self):
        "Two unrelated calls to the procedure must not share results"
        p1 = ConstantProcedure(90, title="The price of the shoes")
        self.assertIsNot(p1(NULL_DEMAND, EMPTY_ENV), p1(NULL_DEMAND, EMPTY_ENV))

    def test_shared_subresult_does_share(self):
        "Calls to the same procedure in the same context share results"
        p1 = ConstantProcedure(90, title="The price of the shoes")
        p2 = FormulaProcedure(p1, p1, code="#1 + #2")
        result = p2(NULL_DEMAND, EMPTY_ENV)
        self.assertIs(result.subresults[0], result.subresults[1])

    @given(many=integers(min_value=0, max_value=5))
    def test_calling_many_invokes_many(self, many):
        "Unrelated calls to a procedure are all executed"
        p1 = Counter(ConstantProcedure(90, title="The price of the shoes"))
        for _ in range(many):
            p1(NULL_DEMAND, EMPTY_ENV)
        self.assertEqual(p1.call_counts, many)

    @given(many=integers(min_value=2, max_value=5))
    def test_calling_many_shared_invokes_once(self, many):
        "Calls to the same procedure in the same are executed only once"
        p1 = Counter(ConstantProcedure(90, title="The price of the shoes"))
        p2 = FormulaProcedure(
            *(p1 for _ in range(many)), code="+".join(f"#{i}" for i in range(1, many + 1))
        )
        p2(NULL_DEMAND, EMPTY_ENV)
        self.assertEqual(p1.call_counts, 1)

    @given(many=integers(min_value=2, max_value=5))
    def test_calling_many_equals_invokes_once(self, many):
        "Calls equivalents procedures in the same are executed only once"

        # This actually relies on the implementation of __eq__ of each
        # procedure.  This is why we had to implement __eq__ in Counter.
        # TODO: Generate pricing programs with hypothesis state-machine module
        # so that we can test this for any of the procedures not just
        # ConstantProcedure.

        def proc():
            return Counter(ConstantProcedure(90, title="The price of the shoes"))

        p2 = FormulaProcedure(
            *(proc() for _ in range(many)),
            code="+".join(f"#{i}" for i in range(1, many + 1)),
        )
        p2(NULL_DEMAND, EMPTY_ENV)
        self.assertEqual(sum(p.call_counts for p in p2.procs), 1)

    def test_adr_scenario(self):
        # The pricing program in the ADRs
        p1 = ConstantProcedure(90, title="The price of the shoes")
        p2 = FormulaProcedure(p1, code="#1 * 0.10", title="Tax of 10%")
        p3 = FormulaProcedure(p1, code="#1 * 0.05", title="Insurance of 5%")
        p4 = FormulaProcedure(p1, p2, p3, code="#1 + #2 + #3", title="The total to pay")
        result = p4(NULL_DEMAND, EMPTY_ENV)
        self.assertIs(result.subresults[0], result.subresults[1].subresults[0])
