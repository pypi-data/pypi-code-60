import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SciFin",
    version="0.0.1",
    author="Fabien Nugier",
    author_email="fabien.nugier@outlook.com",
    description="SciFin is a python package for Science and Finance.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SciFin-Team/SciFin",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

