#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Setup script."""
# Imports

# Built-in dependencies

from os import symlink
from os.path import abspath
from sys import version_info
from setuptools import setup, find_packages

# Compatibility check

if version_info[:2] < (3, 4):
    raise RuntimeError('Python version >= 3.4 required')

# Routines

__metadata__ = {}

with open('lib/geodatabr/__init__.py') as package:
    exec(package.read(), __metadata__)  # pylint: disable=exec-used

# Symlink package data
try:
    for filepath in ('LICENSE', 'data'):
        symlink(abspath(filepath), abspath('lib/geodatabr/' + filepath))
except FileExistsError:
    pass

setup(
    # Package metadata
    name=__metadata__['__package_name__'],
    version=__metadata__['__version__'],
    description=__metadata__['__description__'],
    license=__metadata__['__license__'],
    url=__metadata__['__url__'],
    author=__metadata__['__author_name__'],
    author_email=__metadata__['__author_email__'],

    # Package distribution
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
    package_data={'': ['LICENSE', 'data/stubs/*', 'data/translations/*']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'geodatabr = geodatabr.__main__:main'
        ],
    },

    # Package dependencies
    python_requires='>=3.4',
    install_requires=[
        # geodatabr package
        'requests',
        'ratelimit',
        # geodatabr.dataset package
        'sqlalchemy',
        # geodatabr.encoders package
        'fdb',
        'lxml',
        'msgpack',
        'py-ubjson',
        'pyexcel-ods',
        'pyexcel-xls',
        'pyexcel-xlsx',
        'pyyaml',
    ],
)
