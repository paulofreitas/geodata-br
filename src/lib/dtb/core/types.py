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

import json

from struct import Struct as _Struct

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


class Bytes(bytes):
    '''An improved bytes type.'''

    def unpack(self, _format):
        '''Unpacks data from a binary string according to the given format.

        Arguments:
            _format (str): The pack format
        '''
        compiled_format = _Struct(_format)

        return compiled_format.unpack_from(self) \
            + (self[compiled_format.size:],)


class Struct(dict):
    '''An improved dictionary that provides attribute-style access to keys.'''

    def __getitem__(self, key):
        '''Magic method to proxy nested dictionaries.

        Arguments:
            key (str): The dictionary key to access

        Returns:
            The dictionary key

        Raises:
            KeyError: When a given key is not found
        '''
        value = super(self.__class__, self).__getitem__(key)

        if isinstance(value, dict):
            return self.__class__(value)

        return value

    def __getattr__(self, key):
        '''Magic method to allow accessing dictionary keys as attributes.

        Arguments:
            key (str): The dictionary key to access

        Returns:
            The dictionary key

        Raises:
            AttributeError: When a given key is not found
        '''
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        '''Magic method to allow assigning dictionary keys with attributes.

        Arguments:
            key (str): The dictionary key to change
            value: The value to set
        '''
        self[key] = value

    def __delattr__(self, key):
        '''Magic method to allow deleting dictionary keys with attributes.

        Arguments:
            key (str): The dictionary key to delete

        Raises:
            AttributeError: When a given key is not found
        '''
        try:
            del self[key]
        except KeyError:
            raise AttributeError(key)

    def __repr__(self):
        '''Returns a string representation of this object.

        Returns:
            str: A string representation of this object
        '''
        return '{}({})'.format(self.__class__.__name__, dict.__repr__(self))

    def copy(self):
        '''Copies the self data into a new Struct instance.

        Returns:
            Struct: A new Struct instance with this instance data
        '''
        return self.__class__(self)

    # Serialization methods

    def toJSON(self):
        '''Serializes this object into a JSON string.

        Returns:
            str: A JSON representation of this object
        '''
        return json.dumps(self)
