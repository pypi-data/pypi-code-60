# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['willing_zg']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.8,<4.0.0', 'djangorestframework>=3.11.0,<4.0.0']

setup_kwargs = {
    'name': 'django-willing-zg',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Bequest, Inc.',
    'author_email': 'oss@willing.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
