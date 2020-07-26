# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gender_bender']

package_data = \
{'': ['*'], 'gender_bender': ['language_models/*', 'language_models/english/*']}

install_requires = \
['EbookLib>=0.17.1,<0.18.0',
 'en_core_web_sm @ '
 'https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz',
 'gender-guesser>=0.4.0,<0.5.0',
 'spacy>=2.3.2,<3.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'titlecase>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'gender-bender',
    'version': '0.1.0',
    'description': 'Flips the gender in a text snippet or epub',
    'long_description': None,
    'author': 'Garrett-R',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
