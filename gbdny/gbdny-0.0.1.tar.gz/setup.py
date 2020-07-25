import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gbdny", # Replace with your own username
    version="0.0.1",
    author="Nicolas yanez",
    author_email="n.yanez615@gmail.com",
    description="A small example package for gaussian and binomial distributions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)