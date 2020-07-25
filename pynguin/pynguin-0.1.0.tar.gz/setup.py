# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynguin',
 'pynguin.analyses',
 'pynguin.analyses.controlflow',
 'pynguin.analyses.seeding',
 'pynguin.ga',
 'pynguin.ga.fitnessfunctions',
 'pynguin.ga.operators',
 'pynguin.ga.operators.crossover',
 'pynguin.ga.operators.selection',
 'pynguin.generation',
 'pynguin.generation.algorithms',
 'pynguin.generation.algorithms.randoopy',
 'pynguin.generation.algorithms.wspy',
 'pynguin.generation.export',
 'pynguin.generation.stoppingconditions',
 'pynguin.instrumentation',
 'pynguin.setup',
 'pynguin.testcase',
 'pynguin.testcase.execution',
 'pynguin.testcase.statements',
 'pynguin.testcase.variable',
 'pynguin.testsuite',
 'pynguin.typeinference',
 'pynguin.utils',
 'pynguin.utils.generic',
 'pynguin.utils.statistics']

package_data = \
{'': ['*']}

install_requires = \
['astor>=0.8.1,<0.9.0',
 'bytecode>=0,<1',
 'jellyfish>=0.7.2,<0.8.0',
 'monkeytype>=19.11.2,<20.0.0',
 'networkx[pydot]>=2.4,<3.0',
 'simple-parsing>=0,<1',
 'typing_inspect>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['pynguin = pynguin.cli:main']}

setup_kwargs = {
    'name': 'pynguin',
    'version': '0.1.0',
    'description': 'An automated Python unit test generation tool',
    'long_description': '# Pynguin\n\n[![Build Status](https://gitlab.infosun.fim.uni-passau.de/lukasczy/pynguin/badges/master/pipeline.svg)](https://gitlab.infosun.fim.uni-passau.de/lukasczy/pynguin/pipelines)\n[![Coverage](https://gitlab.infosun.fim.uni-passau.de/lukasczy/pynguin/badges/master/coverage.svg)](https://gitlab.infosun.fim.uni-passau.de/lukasczy/pynguin/pipelines)\n[![License LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org)\n\nPynguin,\nthe\nPYthoN\nGeneral\nUnIt\ntest\ngeNerator,\nis a tool that allows developers to generate unit tests automatically.\n\nIt provides different algorithms to generate sequences that can be used to test your\ncode.\nIt currently does not generate any assertions though.\n\n## Prerequisites\n\nBefore you begin, ensure you have met the following requirements:\n- You have installed Python 3.8\n- You have a recent Linux/macOS machine.  We have not tested the tool on Windows\n  machines although it might work.\n \n## Installing Pynguin\n\nPynguin can be easily installed using the `pip` tool by typing:\n```bash\npip install pynguin\n```\n\nMake sure that your version of `pip` is the one of the Python 3.8 interpreted or a\nvirtual environment that uses Python 3.8 as its interpreter as any older version is\nnot supported by Pynguin!\n\n## Using Pynguin\n\nTODO: Write this section!\n\n## Contributing to Pynguin\n\nFor the development of Pynguin you will need the [`poetry`](https://python-poetry.org)\ndependency management and packaging tool.\nTo start developing, follow these steps:\n1. Clone the repository\n2. Change to the `pynguin` folder: `cd pynguin`\n3. Create a virtual environment and install dependencies using `poetry`: `poetry install`\n4. Make your changes\n5. Run `poetry shell` to switch to the virtual environment in your current shell\n6. Run `make check` to verify that your changes pass all checks\n\n   Please see the `poetry` documentation for more information on this tool.\n   \n### Development using PyCharm.\n\nIf you want to use the PyCharm IDE you have to set up a few things:\n1. Import pynguin into PyCharm.\n2. Find the location of the virtual environment by running `poetry env info` in the project directory.\n3. Go to `Settings` / `Project: pynguin` / `Project interpreter`\n4. Add and use a new interpreter that points to the path of the virtual environment\n5. Set the default test runner to `pytest`\n\n## License\n\nThis project is licensed under the terms of the\n[GNU Lesser General Public License](LICENSE).\n',
    'author': 'Stephan Lukasczyk',
    'author_email': 'stephan@lukasczyk.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pytesting/pynguin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
