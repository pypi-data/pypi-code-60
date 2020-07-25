# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mercs',
 'mercs.algo',
 'mercs.composition',
 'mercs.core',
 'mercs.graph',
 'mercs.utils',
 'mercs.visuals']

package_data = \
{'': ['*'], 'mercs.utils': ['data/*']}

install_requires = \
['catboost>=0.23.2,<0.24.0',
 'dask>=2.21.0,<3.0.0',
 'decision-tree-morfist>=0.1.5,<0.2.0',
 'joblib>=0.16.0,<0.17.0',
 'lightgbm>=2.3.1,<3.0.0',
 'networkx>=2.4,<3.0',
 'numpy>=1.19.1,<2.0.0',
 'scikit-learn>=0.23.1,<0.24.0',
 'shap>=0.35.0,<0.36.0']

setup_kwargs = {
    'name': 'mercs-mixed',
    'version': '0.0.41',
    'description': 'MERCS: Multi-Directional Ensembles of Regression and Classification treeS',
    'long_description': None,
    'author': 'Andrés Reverón Molina',
    'author_email': 'andres@reveronmolina.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
