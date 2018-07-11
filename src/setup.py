#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Setup script."""
# Imports

# Built-in dependencies

import sys

# External dependencies

import setuptools

# Compatibility check

if sys.version_info[:2] < (3, 4):
    raise RuntimeError('Python version >= 3.4 required')

# Routines

__metadata__ = {}

with open('geodatabr/__meta__.py') as package:
    exec(package.read(), __metadata__)  # pylint: disable=exec-used

setuptools.setup(
    # Package metadata
    name=__metadata__['__package_name__'],
    version=__metadata__['__version__'],
    description=__metadata__['__description__'],
    license=__metadata__['__license__'],
    url=__metadata__['__url__'],
    author=__metadata__['__author_name__'],
    author_email=__metadata__['__author_email__'],

    # Package distribution
    packages=setuptools.find_packages(),
    package_data={
        '': ['data/*', 'data/stubs/*', 'data/translations/*'],
        '.': ['LICENSE']
    },
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
        'pytest',
        'ratelimit',
        'requests',
        # geodatabr.core package
        'datapackage',
        'pyyaml',
        # geodatabr.dataset package
        'sqlalchemy',
        # geodatabr.encoders package
        'lxml',
        'pyexcel-ods',
        'pyexcel-xls',
        'pyexcel-xlsx',
    ],
)
