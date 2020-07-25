#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import pytest

from travertine import ExternalObject


class Extended(ExternalObject):
    pass


class Gullible:
    def __eq__(self, other):
        if isinstance(other, ExternalObject):
            return True
        return NotImplemented


def test_external_object_size():
    with pytest.raises(OverflowError):
        ExternalObject("", 2 ** 65 + 1)


def test_comparasion():
    obj1, obj2 = ExternalObject("name", 1), Extended("name", 1)
    with pytest.raises(TypeError):
        obj1 <= obj2
    with pytest.raises(TypeError):
        obj1 < obj2
    with pytest.raises(TypeError):
        obj1 > obj2
    with pytest.raises(TypeError):
        obj1 >= obj2
    assert obj1 == obj2

    g = Gullible()
    with pytest.raises(TypeError):
        assert obj1 == g
    assert g == obj1


def test_from_tuple():
    assert ExternalObject.from_tuple(("name", 1)) == ExternalObject("name", 1)
    assert ExternalObject.from_tuple(("name", 1)) != ExternalObject("name", 2)
    with pytest.raises(ValueError):
        ExternalObject.from_tuple(())
    with pytest.raises(TypeError):
        ExternalObject.from_tuple((1, 1))
    with pytest.raises(TypeError):
        ExternalObject.from_tuple(("", ""))
    with pytest.raises(TypeError):
        ExternalObject.from_tuple(1)
    with pytest.raises(TypeError):
        ExternalObject.from_tuple(("name", 1)) == ("name", 1)


def test_from_reference_string():
    expected = ExternalObject("name", 1)
    assert ExternalObject.from_reference_string("(name, 1)") == expected
    assert ExternalObject.from_reference_string("name, 1") == expected
    with pytest.raises(ValueError):
        ExternalObject.from_reference_string("")
    with pytest.raises(ValueError):
        ExternalObject.from_reference_string("name, a")


def test_extended_creation():
    assert isinstance(Extended("name", 1), Extended)


@pytest.mark.xfail(
    reason="I haven't implemented those methods so that they keep the PyType", strict=True
)
def test_extended_from_tuple():
    assert isinstance(Extended.from_tuple(("name", 1)), Extended)


@pytest.mark.xfail(
    reason="I haven't implemented those methods so that they keep the PyType", strict=True
)
def test_extended_from_reference_string():
    assert isinstance(Extended.from_reference_string("name, 1"), Extended)
