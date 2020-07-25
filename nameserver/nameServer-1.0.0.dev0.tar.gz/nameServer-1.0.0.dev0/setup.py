import re

from setuptools import setup

with open("nameServer/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

with open("README", mode="r",encoding="utf8") as fh:
    long_description = fh.read()

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="nameServer",
    version=version,
    author="Mr.G",
    author_email="gjlove666@hotmail.com",
    description="one web server FrameWork",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "Werkzeug>=0.15",
        "Jinja2>=2.10.1",
        "itsdangerous>=0.24",
        "click>=5.1",
    ],
    extras_require={"dotenv": ["python-dotenv"]},
)

# python3 -m pip install --user --upgrade setuptools wheel twine
# python3 setup.py sdist bdist_wheel
