# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['interop_clients', 'interop_clients.geo']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.7,<7.0', 'pillow>=7.1.2,<8.0.0', 'requests>=2.22.0,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.7.4,<4.0.0'],
 'geo': ['GDAL>=3.1.0,<4.0.0']}

entry_points = \
{'console_scripts': ['interop = interop_clients.cli:main']}

setup_kwargs = {
    'name': 'suas-interop-clients',
    'version': '0.1.2',
    'description': 'Alternative interop clients for AUVSI SUAS',
    'long_description': None,
    'author': 'NC State Aerial Robotics Club',
    'author_email': 'aerialroboticsclub@ncsu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
