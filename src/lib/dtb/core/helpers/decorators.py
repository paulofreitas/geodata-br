#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Decorators helper module

This module provides a set of useful decorators and other wrap-like utility
functions.
'''
# Imports

# Built-in dependencies

import functools

# Classes


class Cached(object):
    '''
    Cache decorator class for memoizing functions and methods.
    '''

    def __init__(self, func):
        '''
        Constructor. Creates a new Cached object.

        Arguments:
            func: The function/method to memoize
        '''
        from dtb.core.types import Struct

        self._func = func
        self._cache = {}
        self._cache_stats = Struct(hits=0, misses=0)

        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __call__(self, *args):
        '''
        Receives the call to the decorated function/method.

        Arguments:
            args: All the arguments passed to the function/method

        Returns:
            The function/method result
        '''
        try:
            # Hits the cache
            result = self._cache[args]
            self._cache_stats.hits += 1

            return result
        except KeyError:
            # Caches the function/method result
            result = self._func(*args)

            self._cache[args] = result
            self._cache_stats.misses += 1

            return result
        except TypeError:
            # Skips caching for non-hashable arguments
            return self._func(*args)

    def __get__(self, instance, owner):
        '''
        Handles the special case for methods in classes (instance methods).

        Arguments:
            instance (type): The class that contains the decorated method
        '''
        if instance is None:
            return self._func

        return functools.partial(self.__call__, instance)

    def __repr__(self):
        '''
        Returns the function's docstring.

        Returns:
            str: The function's docstring
        '''
        return repr(self._func)

    @property
    def stats(self):
        '''
        Reports cache statistics.

        Returns:
            dtb.core.types.Struct: The cache statistics
        '''
        return self._cache_stats

    def invalidate(self):
        '''
        Clears the cache and cache statistics.
        '''
        self._cache.clear()
        self._cache_stats.hits = 0
        self._cache_stats.misses = 0


# Aliases

cached = Cached
