import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
	name = "ihs-dl",
	version = "0.0.2",
	license = "GPLv3",
	description = "IHS Markit Teardown Photo Downloader",
	author = "DerNuntius",
	author_email = "hugo@melder.xyz",
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License (GPL)",
		"Operating System :: OS Independent",
    	],
	platforms = "any",
	install_requires = ["beautifulsoup4"],
	entry_points={'console_scripts': [ 'ihs-dl = ihs_dl:backend', ]}	
)
