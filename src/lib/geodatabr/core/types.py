#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Core types module.

This module provides the base types used across the packages.
"""
# Imports

# Built-in dependencies

import io

from abc import ABCMeta
from collections import Iterable, OrderedDict
from functools import reduce
from random import sample, shuffle
from struct import pack, unpack
from typing import Any, Callable

# Package dependencies

from geodatabr.core.helpers.bootstrapping import ModuleLoader

# Classes


class AbstractClass(object, metaclass=ABCMeta):
    """Base abstract class."""

    @classmethod
    def parent(cls):
        """
        Returns the parent class (metaclass) of this class.

        Returns:
            type: The parent class of this class
        """
        return cls.__class__

    @classmethod
    def childs(cls, forceLoad: bool = True) -> list:
        """
        Returns a list of child classes (subclasses) of this class.

        Args:
            forceLoad: Forces the loading of the given class childs

        Returns:
            The child classes of this class
        """
        if forceLoad:
            ModuleLoader.loadModules(cls.__module__)

        return type.__subclasses__(cls)


class Singleton(object):
    """
    Singleton pattern implementation.

    Attributes:
        _instance: The singleton instance
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton method.

        Args:
            cls (object): The class to get the instance
        """
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)

        return cls._instance


class Bytes(io.BytesIO):
    """An object-oriented bytes type."""

    def _pack(self, _format: str, value: Any):
        """
        Packs a value using the given format.

        Args:
            _format: The packing format
            value: The value to pack
        """
        self.write(pack(_format, value))

    def _unpack(self, _format: str, size: int) -> Any:
        """
        Unpacks a value using the given format.

        Args:
            _format: The packing format
            size: The value size

        Returns:
            The unpacked value
        """
        return unpack(_format, self.read(size))[0]

    def readByte(self) -> int:
        """
        Reads a byte value.

        Returns:
            The byte value
        """
        return ord(self._unpack('c', 1))

    def readBoolean(self) -> bool:
        """
        Reads a boolean value.

        Returns:
            The boolean value
        """
        return self.readByte() == 1

    def readInt(self) -> int:
        """
        Reads an integer value.

        Returns:
            The integer value
        """
        return self._unpack('!i', 4)

    def readFloat(self) -> float:
        """
        Reads a float value.

        Returns:
            The float value
        """
        return self._unpack('!f', 4)

    def readString(self) -> str:
        """
        Reads a string value.

        Returns:
            The string value
        """
        length = self._unpack('i', 4)

        return self._unpack('{:d}s'.format(length), length)

    def writeByte(self, value: int):
        """
        Writes a byte value.

        Args:
            value: The byte value
        """
        self._pack('c', chr(value).encode('utf-8'))

    def writeBoolean(self, value: bool):
        """
        Writes a boolean value.

        Args:
            value: The boolean value
        """
        self.writeByte(1 if value else 0)

    def writeInt(self, value: int):
        """
        Writes an integer value.

        Args:
            value: The integer value
        """
        self._pack('!i', value)

    def writeFloat(self, value: float):
        """
        Writes a float value.

        Args:
            value: The float value
        """
        self._pack('!f', value)

    def writeString(self, value: str):
        """
        Writes a string value.

        Args:
            value: The string value
        """
        length = len(value)

        self._pack('i', length)
        self._pack('{:d}s'.format(length), value)

    def __repr__(self) -> str:
        """
        Returns the canonical string representation of the object.

        Returns:
            The canonical string representation of the object
        """
        return '{:s}({!r})'.format(self.__class__.__name__, self.getvalue())

    def __str__(self) -> str:
        """
        Returns the string representation of the object.

        Returns:
            The string representation of the object
        """
        return str(self.getvalue())

    def __len__(self) -> int:
        """
        Returns the length of the object.

        Returns:
            The length of the object
        """
        return len(self.getvalue())


class BinaryFileStream(io.BytesIO):
    """An in-memory stream for bytes I/O."""

    def __repr__(self) -> str:
        """
        Returns the canonical string representation of the object.

        Returns:
            The canonical string representation of the object
        """
        return '{:s}({!r})'.format(self.__class__.__name__, self.getvalue())

    def __str__(self) -> str:
        """
        Returns the string representation of the object.

        Returns:
            The string representation of the object
        """
        return str(self.getvalue())


class FileStream(io.StringIO):
    """An in-memory stream for string I/O."""

    def __repr__(self) -> str:
        """
        Returns the canonical string representation of the object.

        Returns:
            The canonical string representation of the object
        """
        return '{:s}({!r})'.format(self.__class__.__name__, self.getvalue())

    def __str__(self) -> str:
        """
        Returns the string representation of the object.

        Returns:
            The string representation of the object
        """
        return str(self.getvalue())


class List(list):
    """An improved list type with super powers."""

    def chunk(self, size: int) -> 'List':
        """
        Returns a new list chunked into multiple lists of the given size.

        Args:
            size: The length of each chunk

        Returns:
            A chunked list

        Raises:
            TypeError: If no chunk size is given
            ValueError: If chunk size number is negative
        """
        if size <= 0:
            raise ValueError('The chunk size should be a positive number')

        return List(self[idx:idx + size] for idx in range(0, len(self), size))

    def copy(self) -> 'List':
        """
        Copies the list data into a new List instance.

        Returns:
            A new List instance with this instance data
        """
        return self.__class__(self)

    def difference(self, other: list) -> 'List':
        """
        Returns all of the items that are not present in the other list.

        Args:
            other: The list to compute difference

        Returns:
            A list of different items

        Raises:
            TypeError: If no comparing list is given
            ValueError: If comparing element is not a list
        """
        if not isinstance(other, list):
            raise ValueError('The comparing element is not a list')

        return List(item for item in self if item not in other)

    def filter(self, predicate: Callable) -> 'List':
        """
        Returns all of the items in the list that pass a given truth test.

        Args:
            predicate: The callback function to apply

        Returns:
            A filtered list

        Raises:
            TypeError: If no predicate is given
            ValueError: If predicate is not callable
        """
        if not callable(predicate):
            raise ValueError('The predicate should be callable')

        return List(item for item in self if predicate(item))

    def first(self, predicate: Callable = None) -> Any:
        """
        Returns the first item of the list or the first item in the list that
        passes a given truth test if callback is passed.

        Args:
            predicate: An optional callback function to apply

        Returns:
            The first item of the list

        Raises:
            IndexError: If the list is empty
            ValueError: If predicate is not callable
        """
        if predicate:
            return self.filter(predicate).first()

        return self[0]

    def flatten(self) -> 'List':
        """
        Returns a recursively flattened list from a nested list.

        Returns:
            A flattened list
        """
        flattened = List()

        for item in self:
            flattened.extend(List(item).flatten()
                             if (isinstance(item, Iterable)
                                 and not isinstance(item, (str, bytes))) else
                             [item])

        return flattened

    def intersection(self, other: list) -> 'List':
        """
        Returns all of the common items in both lists, in order.

        Args:
            other: The list to compute intersection

        Returns:
            A list of intersecting items

        Raises:
            TypeError: If no comparing list is given
            ValueError: If comparing element is not a list
        """
        if not isinstance(other, list):
            raise ValueError('The comparing element is not a list')

        return List(item for item in self if item in other)

    def last(self, predicate: Callable = None) -> Any:
        """
        Returns the last item of the list or the last item in the list that
        passes a given truth test if callback is passed.

        Args:
            predicate: An optional callback function to apply

        Returns:
            The last element of the list

        Raises:
            IndexError: If the list is empty
            ValueError: If predicate is not callable
        """
        if predicate:
            return self.filter(predicate).last()

        return self[-1]

    def nth(self, step: int, offset: int = 0) -> 'List':
        """
        Returns a new list consisting of every n-th item.

        Args:
            step: The step size
            offset: The start offset

        Returns:
            A sliced list
        """
        return List([item
                     for position, item in enumerate(self)
                     if position % step == offset])

    def partition(self, predicate: Callable) -> 'List':
        """
        Splits the list into two using the given predicate.

        Args:
            predicate: The callback function to use as predicate

        Returns:
            A partitioned list

        Raises:
            TypeError: If no callback is given
            ValueError: If callback is not callable
        """
        return List([self.filter(predicate), self.reject(predicate)])

    def prepend(self, item: Any):
        """
        Adds an item to the beginning of the list.

        Args:
            item: The item to prepend into list
        """
        self.insert(0, item)

    def reduce(self, predicate: Callable, initial: Any = None) -> Any:
        """
        Reduces the list values into a single value.

        Args:
            predicate: The callback function to apply
            initial: The initial value

        Returns:
            The final reducing value

        Raises:
            TypeError: If no predicate is given
            ValueError: If predicate is not callable
        """
        if not callable(predicate):
            raise ValueError('The predicate should be callable')

        return reduce(predicate, self, initial)

    def reject(self, predicate: Callable) -> 'List':
        """
        Returns all of the items in the list that do not pass a given truth
        test.

        Args:
            predicate: The callback function to apply

        Returns:
            A filtered list

        Raises:
            TypeError: If no predicate is given
            ValueError: If predicate is not callable
        """
        if not callable(predicate):
            raise ValueError('The predicate should be callable')

        return List(item for item in self if not predicate(item))

    def rotate(self, offset: int) -> 'List':
        """
        Returns a new list with items rotated at the given offset.

        Args:
            offset: The offset where the rotation should start

        Returns:
            A rotated list
        """
        return List(self[offset:] + self[:offset])

    def sample(self, count: int = 1) -> 'List':
        """
        Returns a random sample from the list.

        Args:
            count: The number of random items to retrieve from the list

        Returns:
            A random list sample

        Raises:
            ValueError: If the number of random items is negative
        """
        if count < 0:
            raise ValueError('The number of random items should be positive')

        return List(sample(self, count))

    def shift(self) -> Any:
        """
        Removes and return the first item from the list.

        Returns:
            The first item from the list

        Raises:
            IndexError: If the list is empty
        """
        return self.pop(0)

    def shuffle(self) -> 'List':
        """
        Returns a shuffled copy of the list.

        Returns:
            A shuffled copy of the list
        """
        copy = self.copy()
        shuffle(copy)

        return copy

    def splice(self, index: int, size: int = None) -> 'List':
        """
        Removes and returns a slice of items starting at the specified index.

        Args:
            index: The index to start slicing
            size: An optional slice size

        Returns:
            A list of sliced items
        """
        if size:
            _slice = self[index:index + size]
            del self[index:index + size]

            return List(_slice)

        _slice = self[index:]
        del self[index:]

        return List(_slice)

    def split(self, count: int) -> 'List':
        """
        Returns a new list chunked into the given number of groups.

        Args:
            count: The number of groups to split

        Returns:
            A split list

        Raises:
            TypeError: If no number of groups is given
        """
        split = List()

        for idx in reversed(range(1, count + 1)):
            split_idx = len(self) // idx
            split.append(List(self[:split_idx]))
            self = self[split_idx:]

        return split

    def take(self, count: int) -> 'List':
        """
        Returns a new list with the specified number of items.

        Args:
            count: The number of items to take

        Returns:
            A sliced list

        Raises:
            TypeError: If no number of items is given
        """
        return List(self[:count] if count >= 0 else self[count:])

    def transpose(self) -> 'List':
        """
        Returns a transposed list from a nested list.

        Returns:
            A transposed list

        Raises:
            ValueError: If the list is not a nested list
            ValueError: If the list do not have equal sized lists
        """
        if not any(isinstance(item, list) for item in self):
            raise ValueError(
                'The list should be a nested list (a list of lists)')

        if len(set(map(len, self))) != 1:
            raise ValueError('The list should have equal sized lists')

        return List(zip(*self))

    def union(self, other: list) -> 'List':
        """
        Returns all of the unique items in both lists, in order.

        Args:
            other: The list to compute union

        Returns:
            A list of unique items

        Raises:
            TypeError: If no comparing list is given
            ValueError: If comparing element is not a list
        """
        if not isinstance(other, list):
            raise ValueError('The comparing element is not a list')

        return List(self + other).unique()

    def unique(self) -> 'List':
        """
        Returns all of the unique items in the list.

        Returns:
            A list of unique items
        """
        return List(sorted(set(self), key=self.index))

    def __repr__(self) -> str:
        """
        Returns the canonical string representation of the object.

        Returns:
            The canonical string representation of the object
        """
        return '{:s}({!s})'.format(self.__class__.__name__,
                                   super().__repr__())

    # Method aliases

    __and__ = intersection
    __or__ = union
    __sub__ = difference


class Map(dict):
    """An improved dictionary type with attribute-style access."""

    def __getattr__(self, key: Any) -> Any:
        """
        Allows accessing keys as attributes.

        Args:
            key: The mapping key to access

        Returns:
            The mapping key value

        Raises:
            AttributeError: If a given key is not found
        """
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: Any, value: Any):
        """
        Allows assigning keys with attributes.

        Args:
            key: The mapping key to change
            value: The value to set
        """
        self[key] = value

    def __delattr__(self, key: Any):
        """
        Allows deleting mapping keys with attributes.

        Args:
            key: The mapping key to delete

        Raises:
            AttributeError: If a given key is not found
        """
        try:
            del self[key]
        except KeyError:
            raise AttributeError(key)

    def __repr__(self) -> str:
        """
        Returns the canonical string representation of the object.

        Returns:
            The canonical string representation of the object
        """
        return '{}({})'.format(self.__class__.__name__,
                               ', '.join('{}={}'.format(key, repr(value))
                                         for key, value in iter(self.items())))

    def copy(self) -> 'Map':
        """
        Copies the mapping data into a new Map instance.

        Returns:
            A new Map instance with this instance data
        """
        return self.__class__(self)


class OrderedMap(OrderedDict, Map):
    """An improved ordered dictionary type with attribute-style access."""
    pass
