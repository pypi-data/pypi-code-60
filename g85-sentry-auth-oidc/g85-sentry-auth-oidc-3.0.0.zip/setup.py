#!/usr/bin/env python
from __future__ import absolute_import
from setuptools import setup, find_packages


install_requires = [
    'requests<3.0.0'
]


setup(
    name='g85-sentry-auth-oidc',
    version='3.0.0',
    description='OpenID Connect authentication provider for Sentry',
    license='Apache 2.0',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'oidc = oidc.apps.Config',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],
)
