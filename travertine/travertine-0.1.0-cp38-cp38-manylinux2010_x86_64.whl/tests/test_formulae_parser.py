#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import math
import immutables

from hypothesis import given, strategies as st, example

from travertine.formulae import parse, ast
from travertine.procedures import (
    ConstantProcedure,
    FormulaProcedure,
    CeilRoundingProcedure,
)
from travertine.structs import EMPTY_ENV
from travertine.testing.strategies.formulae import expressions

from .tools import PriceCase, NULL_DEMAND, KaboomProcedure


numbers = st.integers(min_value=1, max_value=10 ** 12) | st.floats(
    allow_infinity=False, allow_nan=False, min_value=-10000.0, max_value=10000.0
)


class TestFormulaParser(PriceCase):
    maxDiff = None

    def test_no_substep_zero(self):
        with self.assertRaises(ValueError):
            parse("$0")
        with self.assertRaises(ValueError):
            parse("$01")

    def test_no_unquoted_variable(self):
        with self.assertRaises(ValueError):
            parse("variable")

    def test_regression_no_spaces_before_number(self):
        self.assertEqual(
            parse("#1-6"),
            ast.BinaryOperation(ast.OPERATOR.Sub, ast.Substep(1), ast.LiteralNumber(6)),
        )
        self.assertEqual(parse("---6"), ast.LiteralNumber(-6))
        self.assertEqual(
            parse("#1 - ---6"),
            ast.BinaryOperation(ast.OPERATOR.Sub, ast.Substep(1), ast.LiteralNumber(-6)),
        )

    @given(expressions)
    def test_parse_any_valid_expression(self, expression):
        self.assertEqual(parse(str(expression)), expression)

    def test_basic_formula_with_precedence1(self):
        source = "'variable 1' + #1 * ($2 + 10 - \"variable 2\")"
        self.assertEqual(
            parse(source),
            ast.BinaryOperation(
                ast.OPERATOR.Add,
                ast.Variable("variable 1"),
                ast.BinaryOperation(
                    ast.OPERATOR.Mult,
                    ast.Substep(1),
                    ast.BinaryOperation(
                        ast.OPERATOR.Sub,
                        ast.BinaryOperation(
                            ast.OPERATOR.Add, ast.Substep(2), ast.LiteralNumber(10)
                        ),
                        ast.Variable("variable 2"),
                    ),
                ),
            ),
        )

    def test_basic_formula_with_precedence2(self):
        source = "#1 - #2 - #3"
        self.assertEqual(parse(source), parse("(#1 - #2) - #3"))
        self.assertEqual(
            parse(source),
            ast.BinaryOperation(
                ast.OPERATOR.Sub,
                ast.BinaryOperation(ast.OPERATOR.Sub, ast.Substep(1), ast.Substep(2)),
                ast.Substep(3),
            ),
        )

    def test_basic_formula_with_precedence3(self):
        source = "#1 - (#2 - #3)"
        self.assertEqual(
            parse(source),
            ast.BinaryOperation(
                ast.OPERATOR.Sub,
                ast.Substep(1),
                ast.BinaryOperation(ast.OPERATOR.Sub, ast.Substep(2), ast.Substep(3)),
            ),
        )

    @given(numbers, numbers, numbers, numbers)
    @example(var1=1, s1=64720741412, s2=8186.41788549431, var2=5)
    @example(var1=1, s1=67108865, s2=-2.0000000000020006, var2=4)
    @example(var1=1, s1=8388609, s2=246.58203125000006, var2=5.329070518200753e-11)
    def test_transpiled_basic_formula_with_precedence(self, var1, s1, s2, var2):
        source = "'variable 1' + #1 * ($2 + 10 - \"variable 2\")"

        def model(var1, s1, s2, var2):
            return math.ceil(var1 + s1 * (s2 + 10 - var2))

        environment = immutables.Map({"variable 1": var1, "variable 2": var2})
        proc = CeilRoundingProcedure(
            FormulaProcedure(ConstantProcedure(s1), ConstantProcedure(s2), code=source)
        )
        self.assertPriceMatches(proc(NULL_DEMAND, environment), model(var1, s1, s2, var2))

    @given(numbers, numbers, numbers, numbers)
    @example(var1=1, s1=64720741412, s2=8186.41788549431, var2=5)
    @example(var1=1, s1=67108865, s2=-2.0000000000020006, var2=4)
    @example(var1=1, s1=8388609, s2=246.58203125000006, var2=5.329070518200753e-11)
    def test_transpiled_basic_formula_with_precedence2(self, var1, s1, s2, var2):
        source = "'variable 1' + #1 * ($2 - 10 - \"variable 2\")"

        def model(var1, s1, s2, var2):
            return math.ceil(var1 + s1 * (s2 - 10 - var2))

        environment = immutables.Map({"variable 1": var1, "variable 2": var2})
        proc = CeilRoundingProcedure(
            FormulaProcedure(ConstantProcedure(s1), ConstantProcedure(s2), code=source)
        )
        self.assertPriceMatches(proc(NULL_DEMAND, environment), model(var1, s1, s2, var2))

    def test_unused_procedures_are_not_evaluated(self):
        source = "#1"
        s1 = 10
        proc = FormulaProcedure(ConstantProcedure(s1), KaboomProcedure(), code=source)
        self.assertPriceMatches(proc(NULL_DEMAND, EMPTY_ENV), s1)
