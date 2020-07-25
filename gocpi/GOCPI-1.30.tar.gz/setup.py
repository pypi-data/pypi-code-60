from setuptools import setup
'Note: To upload new versions 1) cd to GOCPI 2) python setup.py sdist 3) twine upload dist/*'
'Note: To download 1) pip install --upgrade GOCPI'
'Note: Make your own python package: https://towardsdatascience.com/make-your-own-python-package-6d08a400fc2d'
'Note: PyPi https://pypi.org/manage/project/gocpi-functions/releases/#modal-close'

setup(name='GOCPI',
      version='1.30',
      description='User Defined Functions and Energy Systems Data for GOCPI Project',
      packages=['GOCPI'],
      author_email='connormcdowall@gmail.com',
      zip_safe=False)
      
'/Users/connor/Google Drive/Documents/University/Courses/2020/ENGSCI 700A&B/GOCPI/src/GOCPI'