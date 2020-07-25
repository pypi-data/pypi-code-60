from setuptools import setup


def readme():
    with open("README.rst") as f:
        return f.read()


setup(
    name="django-sslcommerz",
    version="1.0.0a0",
    description="",
    long_description=readme(),
    # url="https://github.com/monim67/django-sslcommerz",
    # author="Munim Munna",
    # author_email="monim67@yahoo.com",
    license="MIT",
    keywords="",
    packages=["django_sslcommerz"],
    install_requires=["django>=2.0"],
    python_requires=">=3",
    package_data={"django_sslcommerz": []},
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Planning",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 3.0",
    ],
)
