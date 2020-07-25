from setuptools import setup

setup(name='uswapper',
      version='0.40',
      description='Simple wrapper for uniswap graphql api',
      license='MIT',
      packages=['uswapper'],
      install_requires=[
              'pandas',
              'requests==2.22.0',
              'python_graphql_client',
              'six'
              ],
      zip_safe=False)
