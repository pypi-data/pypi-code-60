from setuptools import setup
import setuptools
setup(name='riskmodeler',
      version='1.0',
      description='scorecard build tool',
      url='https://github.com/nothingyang/RiskModeler' ,
      author='Yang xuewen',
      author_email='yangxuewen1234@126.com',
      license='MIT',
      packages=setuptools.find_packages(),
    install_requires=[
                    'datetime',
                    'io',
                    'joblib',
                    'math',
                    'matplotlib',
                    'matplotlib_venn',
                    'numpy',
                    'openpyxl',
                    'os',
                    'pandas',
                    'pandastable',
                    'pickle',
                    'pylab',
                    'random',
                    'seaborn',
                    'sklearn',
                    'statsmodels',
                    'threading',
                    'tkinter'
                    ],
    python_requires='>=3.6',

      zip_safe=False)
