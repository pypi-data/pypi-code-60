#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib3 import Path
from dataclasses import dataclass, field, Field
from sys import path as python_path
import os

p = os.path(__file__)

print(p)


class PathPackError(IOError):
    ''' Error processing PathPack path. '''


class PathPack(Path):
    ''' pathlib.Path subclass to encapsulate more common methods.
    '''
    path_name: (Path) = '.'
    # _path: Field = field(init=False)

    def __i(self):
        Path().__init__()
        # self._path: Path = None
        pass
        # self._path: Path = self.path(self.path_name)

    @property
    def path(self):
        if not self._path:
            self._path = self.path(self.path_name)
        return self._path

    @path.setter
    def path(self, value):
        if isinstance(value, str):
            try:
                self._path = Path(value).resolve()
            except IOError:
                raise PathPackError(
                    f'Error converting {self.path_name} to Path.')
        if not self._path.exists():
            try:
                self._path().touch()
            except IOError:
                raise PathPackError(f'Error creating {self.path_name}')

    @property
    def path_str(self):
        return self.path.as_posix()

    def __str__(self):
        return self.path_str


if __name__ == '__main__':
    p = PathPack('.')

    script_path = Path(__file__).resolve().parents[0]
    here = Path().cwd()

    print(f"script location: {str(script_path[0]):<55.55}")
    print(f"current path:    {str(here):<55.55}")
    print(p)
