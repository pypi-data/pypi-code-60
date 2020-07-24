import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="handyjupyter", # Replace with your own username
    version="0.0.1",
    author="AronWater",
    author_email="kclukac@connect.ust.hk",
    description="Just for convenience when using jupyter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AronWater/handyjupyter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)