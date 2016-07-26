#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
File formats package

This package provides the file format modules.
'''
from __future__ import absolute_import

# Imports

# Built-in dependencies

from abc import ABCMeta as AbstractClass
from itertools import groupby

# External compatibility dependencies

from future.utils import with_metaclass

# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT License'

# Classes


class Format(object, with_metaclass(AbstractClass)):
    '''Abstract file format base class.'''

    @property
    def name(self):
        '''The file format name.'''
        raise NotImplementedError

    @property
    def friendlyName(self):
        '''The file format friendly name.'''
        raise NotImplementedError

    @property
    def extension(self):
        '''The file format extension.'''
        raise NotImplementedError

    @property
    def type(self):
        '''The file format type.'''
        raise NotImplementedError

    @property
    def mimeType(self):
        '''The file format media type.'''
        raise NotImplementedError

    @property
    def info(self):
        '''The file format reference info.'''
        raise NotImplementedError

    def isBinary(self):
        '''Tells whether the file format is binary or not.'''
        return False

    def isParseable(self):
        '''Tells whether the file format is parseable or not.'''
        return False

    def isExportable(self):
        '''Tells whether the file format is exportable or not.'''
        return False

    def isMinifiable(self):
        '''Tells whether the file format is minifiable or not.'''
        return False

    @classmethod
    def instances(cls):
        '''Returns a list with all format classes instances.'''
        return [_format() for _format in cls.__subclasses__()]

    def __str__(self):
        '''Returns a string representation of this format class.'''
        return self.name


class FormatFactory(object):
    '''File format factory class.'''

    @classmethod
    def fromName(cls, name):
        '''Factories a file format class for a given file format name.

        :param name: the file format name to retrieve a file format instance'''
        formats = {_format.name: _format for _format in Format.instances()}

        try:
            return formats[name]
        except KeyError:
            raise UnknownFormatError('No format found with this name: {}' \
                                         .format(name))


class FormatRepository(object):
    '''File format repository class.'''

    @staticmethod
    def findFormatByName(name):
        '''Returns the format with the given name.
        Raises an UnknownFormatError if no format is found.

        :param name: the file format name'''
        for _format in Format.instances():
            if _format.name == name:
                return _format

        raise UnknownFormatError('No format found with this name: {}' \
                                     .format(name))

    @staticmethod
    def findFormatByExtension(extension):
        '''Returns the format with the given extension.
        Raises an UnknownFormatError if no format is found.

        :param extension: the file format extension
        '''
        for _format in Format.instances():
            if _format.extension == extension:
                return _format

        raise UnknownFormatError('No format found with this extension: {}' \
                                     .format(extension))

    @staticmethod
    def findExportableFormats():
        '''Returns a list with all exportable formats.'''
        return [_format for _format in Format.instances()
                if _format.isExportable()]

    @classmethod
    def findExportableFormatNames(cls):
        '''Returns a list with all exportable format names.'''
        return [_format.name for _format in cls.findExportableFormats()]

    @staticmethod
    def findParseableFormats():
        '''Returns a list with all parseable formats.'''
        return [_format for _format in Format.instances()
                if _format.isParseable()]

    @classmethod
    def findParseableFormatNames(cls):
        '''Returns a list with all parseable format names.'''
        return [_format.name for _format in cls.findParseableFormatNames()]

    @staticmethod
    def findMinifiableFormats():
        '''Returns a list with all minifiable formats.'''
        return [_format for _format in Format.instances()
                if _format.isMinifiable()]

    @classmethod
    def findMinifiableFormatNames(cls):
        '''Returns a list with all minifiable format names.'''
        return [_format.name for _format in cls.findMinifiableFormats()]

    @classmethod
    def groupExportableFormatsByType(cls):
        '''Returns a list with all exportable formats grouped by their type.'''
        sorter = lambda _format: _format.type

        return groupby(sorted(cls.findExportableFormats(), key=sorter),
                       key=sorter)


class FormatError(Exception):
    '''Generic exception class for file format errors.'''
    pass


class UnknownFormatError(FormatError):
    '''Exception class raised when a given file format is not found.'''
    pass
