from setuptools import setup, find_packages

setup(
    name='stubwheel',
    version='1.0.5',
    url='https://github.com/AlyShmahell/stubwheel',
    author='AlyShmahell',
    author_email='',
    description='a script that reserves a project name on PyPi',
    packages=['stubwheel'],    
    install_requires=['twine >= 3.2.0'],
    entry_points = {
        "console_scripts": [
            "stubwheel = stubwheel.__main__:main",
        ]
    }
)