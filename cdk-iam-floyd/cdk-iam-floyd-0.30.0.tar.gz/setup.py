import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-iam-floyd",
    "version": "0.30.0",
    "description": "AWS IAM policy statement generator with fluent interface for AWS CDK",
    "license": "Apache-2.0",
    "url": "https://github.com/udondan/iam-floyd",
    "long_description_content_type": "text/markdown",
    "author": "Daniel Schroeder",
    "project_urls": {
        "Source": "https://github.com/udondan/iam-floyd.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_iam_floyd._jsii"
    ],
    "package_data": {
        "cdk_iam_floyd._jsii": [
            "cdk-iam-floyd@0.30.0.jsii.tgz"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.9.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-iam>=1.54.0, <2.0.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
