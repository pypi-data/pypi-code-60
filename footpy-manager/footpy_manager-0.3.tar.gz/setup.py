from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='footpy_manager',
      version='0.3',
      description='A Python package to manage matches of football.',
      packages=['footpy_manager'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)