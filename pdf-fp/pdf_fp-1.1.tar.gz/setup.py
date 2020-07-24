from setuptools import setup

with open("README.md", "r") as fh:
      long_description = fh.read()

setup(name='pdf_fp', version=1.1,
      description='Gaussian and Binomial Distributions',
      packages=['pdf_fp'],
      author = 'Abdelrahman Omran',
      author_email = 'apdo.omran@gmail.com',
      long_description = long_description,
      long_description_content_type = "text/markdown",
      zip_safe=False)