import setuptools
import json
import sys
from urllib import request    
from pkg_resources import parse_version

""""
version : x[Major Fixes].x[Minor Fixes].x[Patch Number].x[Development Version]
"""

def _next_dev_version(pkg_name):
    try:
        url = f'https://pypi.python.org/pypi/{pkg_name}/json'
        releases = json.loads(request.urlopen(url).read())['releases']
        release = sorted(releases, key=parse_version)[-1]
        next_release = release.split('.')
        next_release[-1] = str(int(next_release[-1])+1)
        next_release = ".".join(next_release)
        return next_release
    except:
        return '0.0.0.6'

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line.replace('==','>=') for line in lineiter if line and not line.startswith("#")]


# Constants
REQS = parse_requirements('requirement.txt')
_next_version = _next_dev_version('mlduct')
with open("README.md", "r") as fh:
    long_description = fh.read()


print(setuptools.find_packages())
# Package Setup
setuptools.setup(
    name="mlduct",
    version=_next_version,
    author="Achintya Gupta",
    author_email="ag.ds.bubble@gmail.com",
    description="A personal framework for Machine Learning Pipelines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ag-ds-bubble/mlduct",
    packages=setuptools.find_packages(),
    include_package_data = True,
    install_requires=REQS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)