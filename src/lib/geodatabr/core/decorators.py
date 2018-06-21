#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Core decorators module.

This module provides a set of useful decorators and other wrap-like utility
functions.
"""
# Imports

# Built-in dependencies

import functools

# Classes

class DataDescriptor(type):
    """A data descriptor to allow declaring read-only class properties."""

    def __new__(mcs, name: str, bases: tuple, _dict):
        """
        Creates a new data descriptor.

        Args:
            mcs: The class object to decorate
            name: The class name
            bases: The class base classes
            _dict: The class dictionary of methods/attributes
        """
        class _ReadOnly(mcs):
            pass

        for attr, value in _dict.items():
            if isinstance(value, property):
                setattr(_ReadOnly, attr, value)

        return type.__new__(_ReadOnly, name, bases, _dict)


# Functions


def cachedmethod(maxsize: int = None):
    """
    A cache decorator for memoizing functions and methods.

    Args:
        maxsize: The max cache size. If set, a LRU (least recently used) cache
            is used.

    Returns:
        The cache decorated function
    """
    return functools.lru_cache(maxsize=maxsize)

def datadescriptor(cls):
    """
    A data descriptor decorator to allow declaring read-only class properties.

    Args:
        cls: The class object to decorate

    Returns:
        The decorated class
    """
    return DataDescriptor.__new__(type,
                                  cls.__name__,
                                  cls.__bases__,
                                  dict(cls.__dict__))
