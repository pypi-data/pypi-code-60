#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 'package imports'
import autosys

from autosys import IS_64BITS


class bits:
    def __init__(self, number=0):
        self.data = number

    def __str__(self):
        return str(self.data)

    @property
    def bit1(self):
        return self.data.to_bytes(8, )


def fib(n: int) -> int:
    a, b = 0


b = bits(2)
print(f"{b=}")
print(f"{b.bit1=}")
print(f"{IS_64BITS=}")
