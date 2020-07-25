from setuptools import setup

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='bin-gauss-distros',
      version='0.2',
      description='Binomial and Gaussian Distributions',
      long_description=long_description,
      packages=['bin-gauss-distros'],
      url = 'https://test.pypi.org/project/bin-gauss-distros/',
      author = 'Cristian Iorga',
      author_email = 'ubik3000@gmail.com',
      zip_safe=False)
