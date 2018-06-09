#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Decorators helper module

This module provides a set of useful decorators and other wrap-like utility
functions.
'''
# Imports

# Built-in dependencies

from functools import lru_cache

# Classes


class ClassProperty(object):
    '''
    A data descriptor that allows declaring class properties.
    '''

    def __init__(self, fget):
        '''
        Creates a new ClassProperty descriptor.

        Args:
            fget (callable): The function or method to use to get the value
        '''
        self.fget = fget
        self.fset = None
        self.fdel = None
        self.__doc__ = fget.__doc__

    def __get__(self, instance, owner):
        '''
        Descriptor getter.

        Args:
            instance (object): The property class instance
            owner (class): The property class
        '''
        return self.fget(owner)

    def __set__(self, instance, value):
        '''
        Descriptor setter.

        Args:
            instance (object): The property class instance
            value: The new property value

        Raises:
            AttributeError: When trying to set a class property
        '''
        raise AttributeError("can't set attribute")

    def __delete__(self, instance):
        '''
        Descriptor deleter.

        Args:
            instance (object): The property class instance

        Raises:
            AttributeError: When trying to delete a class property
        '''
        raise AttributeError("can't delete attribute")


# Functions


def cachedmethod(maxsize=None):
    '''
    A cache decorator for memoizing functions and methods.

    Args:
        maxsize (int): The max cache size. If set, a LRU (least recently used)
            cache is used.

    Returns:
        function: The cache decorating function
    '''
    return lru_cache(maxsize=maxsize)


# Aliases

classproperty = ClassProperty
