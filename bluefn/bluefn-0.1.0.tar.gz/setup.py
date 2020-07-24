# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bluefn',
 'bluefn.cli',
 'bluefn.cli.fixtures',
 'bluefn.conf',
 'bluefn.test',
 'bluefn.utils']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.3.1,<0.4.0', 'mako>=1.1.3,<2.0.0', 'typer>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['bluefn = bluefn.__main__:main']}

setup_kwargs = {
    'name': 'bluefn',
    'version': '0.1.0',
    'description': 'toolset for bluechain',
    'long_description': None,
    'author': 'Samlet Wu',
    'author_email': 'xiaofei.wu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
