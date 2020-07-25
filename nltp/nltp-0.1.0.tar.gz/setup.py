import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='nltp',
    version='0.1.0',
    author='Isreal Ufumaka',
    author_email='isrealufumaka@gmail.com',
    description='Simple  automated text preprocessor',
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/izzyx6/nltp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False

)