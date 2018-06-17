#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Core bootstrapping module.

This module provides methods to bootstrap packages and modules.
"""
# Imports

# Built-in dependencies

import sys

from importlib import import_module
from pkgutil import walk_packages

# Classes


class ModuleLoader(object):
    """Module loader class."""

    @staticmethod
    def load(module):
        """
        Loads a given module.

        Args:
            module (str): The module name to load

        Returns:
            module: The given module class
        """
        if module in sys.modules:
            return sys.modules[module]

        return import_module(module)

    @classmethod
    def loadModules(cls, package, ignore_error=True):
        """
        Loads a given package modules.

        Args:
            package: The package name or instance to load modules
            ignore_error (bool): Whether it should ignore import errors or not

        Raises:
            ImportError: When a package module can't be imported
            InvalidPackageError: When a given package is not valid
        """
        if isinstance(package, str):
            package = cls.load(package)

        try:
            namespace = package.__name__ + '.'

            for _, name, _ in walk_packages(package.__path__, namespace):
                cls.load(name)
        except ImportError:
            if not ignore_error:
                raise
        except AttributeError:
            if not ignore_error:
                raise InvalidPackageError(
                    'The given package is not valid: {}'.format(package))


class InvalidPackageError(Exception):
    """Exception class raised when a package is not valid."""
    pass
