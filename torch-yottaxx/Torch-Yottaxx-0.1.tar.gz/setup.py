from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Torch-Yottaxx",
    version="0.1",
    packages=find_packages(),
    author="Yotta",
    author_email="xiaoz987@gmail.com",
    description="a simple autograd library",
    url="https://github.com/Yottaxx",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
