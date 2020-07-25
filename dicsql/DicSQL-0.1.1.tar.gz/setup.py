from distutils.core import setup
setup(
  name = 'DicSQL',         # How you named your package folder (MyLib)
  packages = ['DicSQL'],   # Chose the same as "name"
  version = '0.1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'DicSQL allows you to use SQL database as a dictionary',   # Give a short description about your library
  author = 'Ben Timor',                   # Type in your name
  author_email = 'me@bentimor.com',      # Type in your E-Mail
  url = 'https://github.com/DrBenana/DicSQL',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/DrBenana/DicSQL/archive/v0.1.tar.gz',    # I explain this later on
  keywords = ['DicSQL', 'Dictionary', 'SQL', 'HashMap', 'JSON'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pymysql',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
