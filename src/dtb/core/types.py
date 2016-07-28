#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Core types module

This module provides the base types used across the packages.
'''
# Imports

# Built-in dependencies

from abc import ABCMeta

# External compatibility dependencies

from future.utils import with_metaclass

# Package dependencies

from dtb.core.helpers.bootstrapping import ModuleLoader

# Classes


class AbstractClass(object, with_metaclass(ABCMeta)):
    '''Base abstract class.'''

    @classmethod
    def parent(cls):
        '''Returns the parent class (metaclass) of this class.

        Returns:
            type: The parent class of this class
        '''
        return cls.__class__

    @classmethod
    def childs(cls, forceLoad=True):
        '''Returns a list of child classes (subclasses) of this class.

        Arguments:
            forceLoad (bool): Forces the loading of the given class childs

        Returns:
            list: The child classes of this class
        '''
        if forceLoad:
            ModuleLoader.loadModules(cls.__module__)

        return type.__subclasses__(cls)


class Struct(dict):
    '''A dictionary object which can access/assign/delete keys with attributes.'''

    def __getattr__(self, key):
        '''Magic method to allow accessing dictionary keys as attributes.

        :param key: the dictionary key to access'''
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        '''Magic method to allow assigning dictionary keys with attributes.

        :param key: the dictionary key to change
        :param value: the value to set'''
        self[key] = value

    def __delattr__(self, key):
        '''Magic method to allow deleting dictionary keys with attributes.

        :param key: the dictionary key to delete'''
        del self[key]

    def copy(self):
        '''Copies the self data into a new Struct instance.'''
        return self.__class__(dict.copy(self))
