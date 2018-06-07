#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Core types module

This module provides the base types used across the packages.
'''
# Imports

# Built-in dependencies

import json

from abc import ABCMeta
from collections import OrderedDict
from struct import Struct

# Package dependencies

from geodatabr.core.helpers.bootstrapping import ModuleLoader

# External dependencies

import yaml

# Classes


class AbstractClass(object, metaclass=ABCMeta):
    '''
    Base abstract class.
    '''

    @classmethod
    def parent(cls):
        '''
        Returns the parent class (metaclass) of this class.

        Returns:
            type: The parent class of this class
        '''
        return cls.__class__

    @classmethod
    def childs(cls, forceLoad=True):
        '''
        Returns a list of child classes (subclasses) of this class.

        Arguments:
            forceLoad (bool): Forces the loading of the given class childs

        Returns:
            list: The child classes of this class
        '''
        if forceLoad:
            ModuleLoader.loadModules(cls.__module__)

        return type.__subclasses__(cls)


class Bytes(bytes):
    '''
    An improved bytes type.
    '''

    def unpack(self, _format):
        '''
        Unpacks data from a binary string according to the given format.

        Arguments:
            _format (str): The pack format

        Returns:
            tuple: The unpacked data fields
        '''
        compiled_format = Struct(_format)

        return compiled_format.unpack_from(self) \
            + (self[compiled_format.size:],)


class Map(dict):
    '''
    An improved dictionary that provides attribute-style access to keys.
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructor.
        '''
        super().__init__(*args, **kwargs)

    def __getattr__(self, key):
        '''
        Allows accessing dictionary keys as attributes.

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
        '''
        Allows assigning dictionary keys with attributes.

        Arguments:
            key (str): The dictionary key to change
            value: The value to set
        '''
        self[key] = value

    def __delattr__(self, key):
        '''
        Allows deleting dictionary keys with attributes.

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
        '''
        Returns a string representation of this object.

        Returns:
            str: A string representation of this object
        '''
        return '{}({})'.format(self.__class__.__name__,
                               ', '.join('{}={}'.format(key, repr(value))
                                         for key, value in iter(self.items())))

    def copy(self):
        '''
        Copies the self data into a new Map instance.

        Returns:
            Map: A new Map instance with this instance data
        '''
        return self.__class__(self)

    # Serialization methods

    def toJSON(self):
        '''
        Serializes this object into a JSON string.

        Returns:
            str: A JSON representation of this object
        '''
        return json.dumps(self)

    def toYAML(self):
        '''
        Serializes this object into a YAML string.

        Returns:
            str: A YAML representation of this object
        '''
        from geodatabr.formats.yaml.utils import OrderedDumper

        return yaml.dump(self, Dumper=OrderedDumper)


class OrderedMap(OrderedDict, Map):
    '''
    An improved ordered dictionary that provides attribute-style access to keys.
    '''
    pass


class Singleton(object):
    '''
    Singleton pattern implementation.
    '''
    _instance = None

    def __new__(cls, *args, **kwargs):
        '''
        Singleton method.

        Arguments:
            cls (object): The class to get the instance
        '''
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)

        return cls._instance
