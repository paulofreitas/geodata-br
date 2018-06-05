#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Setup script
'''
# Imports

# Built-in dependencies

import sys

from setuptools import setup, find_packages

# Compatibility check

if sys.version_info[:2] < (3, 4):
    raise RuntimeError('Python version >= 3.4 required')

# Routines

with open('lib/geodatabr/__init__.py') as metadata:
    exec(metadata.read())

setup(
    # Package metadata
    name=__name__,
    version=__version__,
    description=__description__,
    license=__license__,
    url=__url__,
    author=__author_name__,
    author_email=__author_email__,

    # Package distribution
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
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
        # geodatabr.exporters package
        'fdb',
        'lxml',
        'msgpack',
        'pyyaml',
        'sqlalchemy',
        # geodatabr.parsers package
        'xlrd',
        'xlwt',
    ]
)
