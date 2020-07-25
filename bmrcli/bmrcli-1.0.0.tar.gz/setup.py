from setuptools import setup, find_packages

with open("requirements.txt", "r") as fh:
    install_requires = [line for line in fh.readlines() if line[0] not in ("#", "-")]

setup(
    name="bmrcli",
    version="1.0.0",
    description="BMR HC64 command-line tool",
    long_description="",
    author="Dan Keder",
    author_email="dan.keder@protonmail.com",
    url="http://github.com/dankeder/bmrcli",
    keywords="bmr hc64 heating home-automation",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={"console_scripts": ["bmrcli = bmrcli:main"]},
)
