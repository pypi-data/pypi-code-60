#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from collections.abc import Mapping
from hypothesis.stateful import rule

from travertine.testing.strategies.programs import ProcedureMachine


class EVMMachine(ProcedureMachine):
    @rule(proc=ProcedureMachine.procedures)
    def check_programs_can_compute_evms(self, proc):
        assert isinstance(proc.evm, Mapping)


EVMCase = EVMMachine.TestCase
