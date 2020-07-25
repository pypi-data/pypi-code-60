import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='bucket_gcp',
    version='1.2',
    install_requires=[
        'Django==3.0.2',
        'google-cloud-storage'
    ],
    packages=find_packages(),
    include_package_data=True,
    description='A simple Django app to upload or download files from gcp bucket.',
    long_description=README,
    url='',
    author='iraj majeed, abeera riaz',
    author_email='iraj@shopdev.co, abeera@shopdev.co',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        # 'Framework :: Django :: X.Y',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
