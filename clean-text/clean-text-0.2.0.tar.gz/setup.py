# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cleantext']

package_data = \
{'': ['*']}

install_requires = \
['ftfy>=5.8,<6.0']

extras_require = \
{'gpl': ['unidecode>=1.1.1,<2.0.0']}

setup_kwargs = {
    'name': 'clean-text',
    'version': '0.2.0',
    'description': 'Functions to preprocess and normalize text.',
    'long_description': None,
    'author': 'Johannes Filter',
    'author_email': 'hi@jfilter.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
