from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'tlingua',
  packages = ['tlingua'],

  version = '000.000.001',
  license='MIT',
  description = 'A little library for text/grammar processing.',
  long_description = long_description,
  long_description_content_type = 'text/markdown',

  author = 'Luduk',
  author_email = 'ningawent@gmail.com',

  url = 'https://github.com/LudwigVonChesterfield/TLingua',
  download_url = 'https://github.com/LudwigVonChesterfield/TLingua/archive/v_000.000.001.tar.gz',

  keywords = ['TAGS', 'STRINGS', 'GRAMMAR', 'LANGUAGE'],

  install_requires=[
  ],

  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)