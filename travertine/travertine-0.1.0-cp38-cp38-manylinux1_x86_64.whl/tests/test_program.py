#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from travertine import Program, create_program, UnitaryDemand
from travertine.types import TypedAttribute, SimpleType, TypeName, Undefined
from travertine.procedures import (
    ConstantProcedure,
    FormulaProcedure,
    GetAttributeProcedure,
)

from travertine.testing.strategies.programs import ProgramMachine

from hypothesis import given, strategies as st
from hypothesis.stateful import run_state_machine_as_test


@given(st.floats(allow_infinity=False, allow_nan=False))
def test_add_constant(value):
    program = Program()
    ConstantProcedure(value).add_to_travertine_program(program)
    assert program.execute(UnitaryDemand.default(), Undefined) == value


@given(st.lists(st.floats(allow_infinity=False, allow_nan=False), min_size=2))
def test_add_constants_and_execute_last(values):
    program = Program(len(values))
    # I need to collect every procedure or Python could GC collect some
    # instances of ConstantProcedure and reuse an index.
    procedures = []
    for value in values:
        procedures.append(ConstantProcedure(value))
        procedures[-1].add_to_travertine_program(program)
    assert program.execute(UnitaryDemand.default(), Undefined) == values[-1]


@given(
    st.floats(allow_infinity=False, allow_nan=False),
    st.floats(allow_infinity=False, allow_nan=False).filter(bool),
    st.sampled_from(["+", "-", "*", "/"]),
)
def test_formula_procedure(v1, v2, operation):
    c1 = ConstantProcedure(v1)
    c2 = ConstantProcedure(v2)
    formula = FormulaProcedure(c1, c2, code=f"#1 {operation} #2")
    program = create_program(formula)
    if operation == "+":
        expected = v1 + v2
    elif operation == "-":
        expected = v1 - v2
    elif operation == "*":
        expected = v1 * v2
    elif operation == "/":
        expected = v1 / v2
    assert program.execute_many(
        [UnitaryDemand.default(), UnitaryDemand.default()], Undefined
    ) == [expected, expected]


typenames = st.from_type(TypeName).filter(lambda t: t != TypeName.UNKNOWN)
simpletypes = st.builds(SimpleType, typenames)
attrs = st.builds(TypedAttribute, st.sampled_from(["attr1", "attr2"]), simpletypes)


@given(attrs, st.floats(allow_infinity=False, allow_nan=False))
def test_execute_getting_attr(attr, value):
    null = UnitaryDemand.default()
    demand = null.replace_attr(attr.name, value)
    assert demand.attr(attr.name) == value
    procedure = GetAttributeProcedure(attr)
    program = create_program(procedure)
    assert program.execute_many([null, demand], Undefined) == [Undefined, value]


def test_cant_add_twice_the_same_procedure():
    program = Program()
    procedure = ConstantProcedure(10)
    procedure.add_to_travertine_program(program)
    try:
        procedure.add_to_travertine_program(program)
    except ValueError:
        pass
    else:
        raise AssertionError("Should have raised a ValueError")


def test_arbitrary_programs_can_be_created():
    run_state_machine_as_test(ProgramMachine)
