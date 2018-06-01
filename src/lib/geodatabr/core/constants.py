#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Core constants module

This module provides the core constants.
'''
# Imports

# Package dependencies

from geodatabr.core.helpers.filesystem import Directory, Path

# Constants

PKG_DIR = Directory(Path(__file__).parents[1])
LIB_DIR = Directory(PKG_DIR.parent)
SRC_DIR = Directory(LIB_DIR.parent)
BASE_DIR = Directory(SRC_DIR.parent)
DATA_DIR = Directory(Path().cwd())
