# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stormlock', 'stormlock.backends']

package_data = \
{'': ['*']}

extras_require = \
{'dynamodb': ['boto3>=1.13.1,<2.0.0'],
 'etcd': ['etcd3>=0.12.0,<0.13.0'],
 'postgresql': ['psycopg2>=2.8.5,<3.0.0'],
 'redis': ['redis>=3.4.1,<4.0.0']}

entry_points = \
{'console_scripts': ['stormlock = stormlock.cli:run'],
 'stormlock.backends': ['dynamodb = stormlock.backends.dynamodb:DynamoDB '
                        '[dynamodb]',
                        'etcd = stormlock.backends.etcd:Etcd [etcd]',
                        'postgresql = stormlock.backends.postgresql:Postgresql '
                        '[postgresql]',
                        'redis = stormlock.backends.redis:Redis [redis]']}

setup_kwargs = {
    'name': 'stormlock',
    'version': '0.1.0',
    'description': 'Simple distributed lock with support for multiple backends',
    'long_description': None,
    'author': 'Thayne McCombs',
    'author_email': 'astrothayne@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
