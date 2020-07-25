from pathlib import Path
import setuptools

long_description = Path('README.md').read_text()

setuptools.setup(
    name='pyquine',
    version='0.1',
    author='Gramkraxor',
    author_email='gram@krax.dev',
    url='https://github.com/gramkraxor/pyquine',
    description='The best `import quine`',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['quine'],
    license='Unlicense',
    classifiers=[
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3',
    py_modules=['quine'],
)
