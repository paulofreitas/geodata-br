#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Core package.

This package provides all the reusable stuff used in other packages.
"""
# Package imports

from geodatabr.core.helpers.filesystem import Directory, Path

# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2018 Paulo Freitas'
__license__ = 'MIT License'

# Constants

PKG_DIR = Directory(Path(__file__).parents[1])
LIB_DIR = Directory(PKG_DIR.parent)
SRC_DIR = Directory(LIB_DIR.parent)
BASE_DIR = Directory(SRC_DIR.parent)
DATA_DIR = Directory(Path().cwd())
