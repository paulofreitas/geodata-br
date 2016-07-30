#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Core constants module

This module provides the core constants.
'''
# Imports

# Built-in dependencies

from os.path import abspath, dirname, join as path

# Constants

PKG_DIR = abspath(path(dirname(__file__), '..'))
LIB_DIR = abspath(path(PKG_DIR, '..'))
SRC_DIR = abspath(path(LIB_DIR, '..'))
BASE_DIR = abspath(path(SRC_DIR, '..'))
DATA_DIR = path(BASE_DIR, 'data')
