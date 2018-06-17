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
from types import ModuleType
from typing import Any

# Classes


class ModuleLoader(object):
    """Module loader class."""

    @staticmethod
    def load(module: str) -> ModuleType:
        """
        Loads a given module.

        Args:
            module: The module name to load

        Returns:
            The given module class

        Raises:
            ModuleNotFoundError: Raised when a module could not be located
            ImportError: Raised when the a module could not be loaded
        """
        if module in sys.modules:
            return sys.modules[module]

        try:
            return import_module(module)
        except ImportError:
            raise ModuleNotFoundError("No module named '{}'".format(module))
        except Exception:
            raise ImportError("Failed to load module '{}'".format(module))

    @classmethod
    def loadModules(cls, package: Any, ignore_error: bool = True):
        """
        Loads a given package modules.

        Args:
            package: The package name or instance to load modules
            ignore_error: Whether it should ignore import errors or not

        Raises:
            ModuleNotFoundError: Raised when a module could not be located
            ImportError: Raised when the a module could not be loaded
        """
        try:
            if isinstance(package, str):
                package = cls.load(package)

            namespace = package.__name__ + '.'

            for _, name, _ in walk_packages(package.__path__, namespace):
                cls.load(name)
        except AttributeError:
            raise ModuleNotFoundError("No module named '{}'".format(package))
        except Exception:
            if not ignore_error:
                raise


class ModuleNotFoundError(ImportError):
    """Exception class raised when a module could not be located."""
