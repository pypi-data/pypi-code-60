"""Setup script for NBA Stats API Python client.

Also installs included versions of third party libraries, if those libraries
are not already installed
"""
import sys

if sys.version_info < (3, 8):
    print("python-nbaclient requires python version >= 3.8.", file=sys.stderr)
    sys.exit(1)

import io
import os
from setuptools import setup, find_packages

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.md")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

install_requires = [
    "requests",
    "pprint"
]

version = "0.0.7"

setup(
    name="python_nbaclient",
    version=version,
    author="Lucas H. Xu",
    author_email="lucasxu.pub@gmail.com",
    description="A Python Wrapper of NBA RESTful Stats APIs",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/xuhang57/python_nbaclient",
    packages=find_packages(),
    license="GPLv3",
    keywords="nba python client api",
    install_requires=install_requires,
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
