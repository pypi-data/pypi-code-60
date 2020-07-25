#!/usr/bin/env python3


import setuptools


def version():
    with open('VERSION', 'r') as f:
        return f.read()


if __name__ == '__main__':
    setuptools.setup(version=version())
