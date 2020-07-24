#!/usr/bin/python -tt

import os
from setuptools import setup


def detect_bad_upgrade():
    # prevent direct upgrade from 2.9.x or earlier to 2.10 due to pip limitations
    try:
        import ansible
    except ImportError:
        # ansible is not installed
        return False

    try:
        current_version = ansible.__version__.split('.')
    except AttributeError:
        # ansible is installed but already broken.  We're probably being reinstalled.
        return False

    try:
        current_version = (int(current_version[0]), int(current_version[1]))
    except Exception as e:
        print("""\n
            ### ERROR ###

            The currently installed ansible is of an unknown version.  Since upgrading directly
            from ansible-2.9 or less to ansible-2.10 with pip is known to cause problems, please
            uninstall the old version and install the new version:

                pip uninstall ansible
                pip install ansible

            If you have a broken installation, perhaps because ansible-base was installed before
            ansible was upgraded, try this to resolve it:

                pip install --force-reinstall ansible ansible-base

            If you want to install anyways and cleanup any breakage afterwards, set the
            ANSIBLE_SKIP_CONFLICT_CHECK environment variable:

                ANSIBLE_SKIP_CONFLICT_CHECK=1 pip install ansible

            ### END ERROR ###

            """)
    else:
        if current_version >= (2, 10):
            return False

        print("""\n
            ### ERROR ###

            Upgrading directly from ansible-2.9 or less to ansible-2.10 or greater with pip is
            known to cause problems.  Please uninstall the old version and install the new version:

                pip uninstall ansible
                pip install ansible

            If you have a broken installation, perhaps because ansible-base was installed before
            ansible was upgraded, try this to resolve it:

                pip install --force-reinstall ansible ansible-base

            If you want to install anyways and cleanup any breakage afterwards, set the
            ANSIBLE_SKIP_CONFLICT_CHECK environment variable:

                ANSIBLE_SKIP_CONFLICT_CHECK=1 pip install ansible

            ### END ERROR ###

            """)

    return True


if not os.environ.get('ANSIBLE_SKIP_CONFLICT_CHECK'):
    if detect_bad_upgrade():
        sys.exit(1)


__version__ = '2.10.0a4'
__author__ = 'Ansible, Inc.'


with open('README.rst', 'r') as f:
    long_desc = f.read()

setup(
    name='ansible',
    version=__version__,
    description='Radically simple IT automation',
    long_description=long_desc,
    author=__author__,
    author_email='info@ansible.com',
    url='https://ansible.com/',
    project_urls={
        'Bug Tracker': 'https://github.com/ansible/ansible/issues',
        'CI: Shippable': 'https://app.shippable.com/github/ansible/ansible',
        'Code of Conduct': 'https://docs.ansible.com/ansible/latest/community/code_of_conduct.html',
        'Documentation': 'https://docs.ansible.com/ansible/',
        'Mailing lists': 'https://docs.ansible.com/ansible/latest/community/communication.html#mailing-list-information',
        'Source Code': 'https://github.com/ansible/ansible',
    },
    license='GPLv3+',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    packages=['ansible_collections'],
    include_package_data=True,
    install_requires=[
        'ansible-base>=2.10.0b1,<2.11',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    data_files=[],
    # Installing as zip files would break due to references to __file__
    zip_safe=False
)