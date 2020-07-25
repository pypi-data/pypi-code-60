# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['channels_graphql_ws']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.5,<4.0',
 'asgiref>=3.2,<4.0',
 'channels>=2.2,<3.0',
 'django>=2.2,<4',
 'graphene>=2.1,<3.0',
 'graphql-core>=2.2',
 'msgpack>=0.6.1,<2']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'django-channels-graphql-ws',
    'version': '0.6.0',
    'description': 'Django Channels based WebSocket GraphQL server with Graphene-like subscriptions',
    'long_description': None,
    'author': 'Alexander A. Prokhorov',
    'author_email': 'alexander.prokhorov@datadvance.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/datadvance/DjangoChannelsGraphqlWs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
