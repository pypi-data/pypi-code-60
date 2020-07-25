from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='problib',
      version='0.2',
      description='Gaussian and Binomial Probability Distributions',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/lisza/problib',
      license='MIT',
      author='lisza',
      packages=['problib'],
      zip_safe=False)