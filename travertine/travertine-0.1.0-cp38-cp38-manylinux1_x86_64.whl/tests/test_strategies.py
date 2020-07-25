#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import unittest

from hypothesis.stateful import rule

from travertine.structs import EMPTY_ENV
from travertine.testing.strategies.programs import (
    ProcedureMachine as BaseProcedureMachine,
)
from travertine.testing.strategies.structs import demands


class ProcedureMachine(BaseProcedureMachine):
    @rule(proc=BaseProcedureMachine.procedures, demand=demands())
    def check_programs_compute(self, proc, demand):
        proc(demand, EMPTY_ENV)

    @rule(proc=BaseProcedureMachine.branching_procedures)
    def check_generated_branching_procedures_are_well_typed(self, proc):
        assert proc.match_table is not None or proc.interval_tree is not None


ProcedureCase = ProcedureMachine.TestCase
