
import os
import setuptools

from setuptools import setup
from textwrap import dedent

__version__ = '1.1.1'
__release__ = '$release 39'

long_description = 'https://github.com/michael-ross-ven/vengeance/blob/master/README.md\n(specialize this for pypi.org later)'


def __make_gencache_folder():
    try:
        import shutil
        import site

        win32com_folder     = site.getsitepackages()[1] + '\\win32com'
        gencache_folder     = win32com_folder + '\\gen_py'
        old_gencache_folder = os.environ['userprofile'] + '\\AppData\\Local\\Temp\\gen_py\\'

        if os.path.exists(win32com_folder):
            if not os.path.exists(gencache_folder):
                
                os.makedirs(gencache_folder)
                if os.path.exists(old_gencache_folder):
                    shutil.rmtree(old_gencache_folder)
                    
    except Exception:
        pass
        


if __name__ == '__main__':
    setup(name='vengeance',
          version=__version__,
          description='Library focusing on row-major organization of tabular data and control over the Excel application',
          long_description=long_description,
          url='https://github.com/michael-ross-ven/vengeance',
          author='Michael Ross',
          author_email='',
          license='MIT',
          install_requires=('comtypes', 'pypiwin32'),
          extra_require=('numpy', 'python-dateutil', 'ujson', 'line-profiler'),
          packages=setuptools.find_packages(),
          classifiers=[
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: MIT License",
              "Operating System :: Microsoft :: Windows"
            ]

          )

    __make_gencache_folder()

