from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="python_nbaclient",
    version="0.0.3",
    author="Lucas H. Xu",
    author_email="lucasxu.pub@gmail.com",
    description="A Python Wrapper of NBA RESTful Stats APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xuhang57/python_nbaclient",
    packages=find_packages(),
    install_requires=['requests', 'pprint'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
