#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from dataclasses import dataclass
from typing import Iterable, Tuple

from travertine.topo import topological_sort


@dataclass(unsafe_hash=True)
class Node:
    """Interface for the nodes expected in `topological_sort`:func:.

    The attributes defined simply state that:

    - Those attributes are required in the nodes.
    - The types expected.

    The methods defined are just provided so that testing is possible.

    """

    name: str
    depends: Tuple["Node"]

    def __init__(self, name: str, depends: Iterable["Node"]) -> None:
        self.name = name
        self.depends = depends = tuple(depends)

    def __iter__(self):
        return iter(self.depends)


def test_dag_diamond():
    # A < B, A < C, B < D, C < D
    # possible orders are:
    # A, B, C, D
    # A, C, B, D
    A = Node("A", [])
    B = Node("B", [A])
    C = Node("C", [A])
    D = Node("D", [B, C])
    res = list(topological_sort(D))
    assert res in ([A, B, C, D], [A, C, B, D])


def test_cycle():
    A = Node("A", [])
    B = Node("B", [A])
    C = Node("C", [A])
    D = Node("D", [B, C])
    A.depends += (D,)
    try:
        list(topological_sort(D))
    except RuntimeError:
        pass
    else:
        raise AssertionError("A cycle should have been detected")
