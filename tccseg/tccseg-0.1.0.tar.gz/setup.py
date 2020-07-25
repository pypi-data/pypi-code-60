from setuptools import setup



MAJOR = 0
MINOR = 1
MICRO = 0
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

with open('README.md') as f:
    long_description = f.read()

setup(
    name='tccseg',
    packages=['tccseg'],
    version=VERSION,
    license='MIT',
    description='Thai Character Cluster segmentation python package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Thodsaporn Chay-intr',
    author_email='chayintr@lr.pi.titech.ac.jp',
    url='https://github.com/tchayintr/tccseg',
    keywords=['tcc', 'segmentation', 'Thai'],
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
