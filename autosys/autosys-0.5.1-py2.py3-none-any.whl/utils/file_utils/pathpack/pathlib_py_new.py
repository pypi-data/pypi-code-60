#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from dataclasses import dataclass, field, Field
from os import linesep as NL

vars_width = len(max(vars(Path))) + 2


@dataclass
class VarsList:
    obj: Field = field()

#     def __str__(self):
#         return str(object())


v = VarsList(Path)
print(v)
print(v.__dict__.items())

print(vars_width)
vars_list = NL.join(
    [f"{k:<{vars_width}.{vars_width}}:  {v}" for k, v in vars(Path).items()])
print(vars_list)
