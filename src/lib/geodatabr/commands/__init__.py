#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Commands package.

This package provides the available command modules.
"""
# Package imports

from geodatabr import __author__, __copyright__, __license__, __version__
from geodatabr.core.bootstrapping import ModuleLoader

ModuleLoader.loadModules(__package__)

# Package exports

__all__ = [
    '__author__',
    '__copyright__',
    '__license__',
    '__version__',
]
