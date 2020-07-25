import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Password-validate",
    version="1.0.0",
    description="Validate user passwords on the go",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Devcyclops/password_validator",
    author="Kennedythacode",
    author_email="johnkennedyx1212@gmail.com",
    download_url = 'https://github.com/Devcyclops/password_validator/archive/1.0.0.tar.gz',
    license="Apache",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
)
