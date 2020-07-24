import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrustic",
    version="0.0.1",
    author="Alex Rustic",
    author_email="pyrustic@protonmail.com",
    description="Short description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyrustic/pyrustic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
