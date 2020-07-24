# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyson']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-json',
    'version': '0.1.1',
    'description': '',
    'long_description': '# pyson\nThe definitive extension to the core python json module\n',
    'author': 'Shparki',
    'author_email': 'matt.murray@pnmac.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shparki/pyson',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
