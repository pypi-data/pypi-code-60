# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['panos']

package_data = \
{'': ['*']}

install_requires = \
['pan-python>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'pan-os-python',
    'version': '1.0.0b1',
    'description': 'Framework for interacting with Palo Alto Networks devices via API',
    'long_description': '========================================\nPalo Alto Networks PAN-OS SDK for Python\n========================================\n\nThe PAN-OS SDK for Python (pan-os-python) is a package to help interact with\nPalo Alto Networks devices (including physical and virtualized Next-generation\nFirewalls and Panorama).  The pan-os-python SDK is object oriented and mimics\nthe traditional interaction with the device via the GUI or CLI/API.\n\n* Documentation: http://pan-os-python.readthedocs.io\n* Overview: http://paloaltonetworks.github.io/pan-os-python\n* Free software: ISC License\n\n-----\n\n|pypi| |rtd| |gitter|\n\n-----\n\nFeatures\n--------\n\n- Object model of Firewall and Panorama configuration\n- Multiple connection methods including Panorama as a proxy\n- All operations natively vsys-aware\n- Support for high availability pairs and retry/recovery during node failure\n- Batch User-ID operations\n- Device API exception classification\n\nStatus\n------\n\nPalo Alto Networks PAN-OS SDK for Python is considered stable. It is fully tested\nand used in many production environments. Semantic versioning is applied to indicate\nbug fixes, new features, and breaking changes in each version.\n\nInstall\n-------\n\nInstall using pip::\n\n    pip install pan-os-python\n\nUpgrade to the latest version::\n\n    pip install --upgrade pan-os-python\n\nIf you have poetry installed, you can also add pan-os-python to your project::\n\n    poetry add pan-os-python\n\nHow to import\n-------------\n\nTo use pan-os-python in a project::\n\n    import panos\n\nYou can also be more specific about which modules you want to import::\n\n    from panos import firewall\n    from panos import network\n\n\nA few examples\n--------------\n\nFor configuration tasks, create a tree structure using the classes in\neach module. Nodes hierarchy must follow the model in the\n`Configuration Tree`_.\n\nThe following examples assume the modules were imported as such::\n\n    from panos import firewall\n    from panos import network\n\nCreate an interface and commit::\n\n    fw = firewall.Firewall("10.0.0.1", api_username="admin", api_password="admin")\n    eth1 = network.EthernetInterface("ethernet1/1", mode="layer3")\n    fw.add(eth1)\n    eth1.create()\n    fw.commit()\n\nOperational commands leverage the \'op\' method of the device::\n\n    fw = firewall.Firewall("10.0.0.1", api_username="admin", api_password="admin")\n    print fw.op("show system info")\n\nSome operational commands have methods to refresh the variables in an object::\n\n    # populates the version, serial, and model variables from the live device\n    fw.refresh_system_info()\n\nSee more examples in the `Usage Guide`_.\n\n\nContributors\n------------\n\n- Brian Torres-Gil - `github <https://github.com/btorresgil>`__\n- Garfield Freeman - `github <https://github.com/shinmog>`__\n- John Anderson - `github <https://github.com/lampwins>`__\n- Aditya Sripal - `github <https://github.com/AdityaSripal>`__\n\nThank you to Kevin Steves, creator of the pan-python library:\n    https://github.com/kevinsteves/pan-python\n\n\n.. _pan-python: http://github.com/kevinsteves/pan-python\n.. _Configuration Tree: http://pan-os-python.readthedocs.io/en/latest/configtree.html\n.. _Usage Guide: http://pan-os-python.readthedocs.io/en/latest/usage.html\n\n.. |pypi| image:: https://img.shields.io/pypi/v/pan-os-python.svg\n    :target: https://pypi.python.org/pypi/pan-os-python\n    :alt: Latest version released on PyPi\n\n.. |rtd| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg\n    :target: http://pan-os-python.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. |coverage| image:: https://img.shields.io/coveralls/PaloAltoNetworks/pan-os-python/master.svg?label=coverage\n    :target: https://coveralls.io/r/PaloAltoNetworks/pan-os-python?branch=master\n    :alt: Test coverage\n\n.. |gitter| image:: https://badges.gitter.im/PaloAltoNetworks/pan-os-python.svg\n    :target: https://gitter.im/PaloAltoNetworks/pan-os-python\n    :alt: Chat on Gitter\n',
    'author': 'Palo Alto Networks',
    'author_email': 'devrel@paloaltonetworks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PaloAltoNetworks/pan-os-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
