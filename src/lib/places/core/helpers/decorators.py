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


class CachedMethod(object):
    '''
    A cache decorator for memoizing functions and methods.
    '''

    def __init__(self, func):
        '''
        Constructor. Creates a new CachedMethod decorator.

        Arguments:
            func (callable): The callable to memoize
        '''
        from places.core.types import Map

        self._func = func
        self._cache = {}
        self._cache_stats = Map(hits=0, misses=0)

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
            places.core.types.Struct: The cache statistics
        '''
        return self._cache_stats

    def invalidate(self):
        '''
        Clears the cache and cache statistics.
        '''
        self._cache.clear()
        self._cache_stats.hits = 0
        self._cache_stats.misses = 0


class ClassProperty(object):
    '''
    A data descriptor that allows declaring class properties.
    '''

    def __init__(self, fget):
        '''
        Constructor. Creates a new ClassProperty descriptor.

        Arguments:
            fget (callable): The function or method to use to get the value
        '''
        self.fget = fget
        self.fset = None
        self.__doc__ = fget.__doc__

    def __get__(self, instance, owner):
        '''
        Descriptor getter.
        '''
        return self.fget(owner)

    def __set__(self, instance, value):
        '''
        Descriptor setter.
        '''
        raise AttributeError("can't set attribute")


# Aliases

cachedmethod = CachedMethod
classproperty = ClassProperty
