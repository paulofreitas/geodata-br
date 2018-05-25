#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
File formats package

This package provides an abstract file format class, a file format factory
class, a file format repository class and concrete file format modules.
'''
from __future__ import absolute_import

# Imports

# Built-in dependencies

from itertools import groupby

# Package dependencies

from places.core.helpers.decorators import classproperty
from places.core.types import AbstractClass

# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2018 Paulo Freitas'
__license__ = 'MIT License'

# Classes


class Format(AbstractClass):
    '''
    Abstract file format base class.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        raise NotImplementedError

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        raise NotImplementedError

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        raise NotImplementedError

    @classproperty
    def type(self):
        '''
        The file format type.
        '''
        raise NotImplementedError

    @classproperty
    def mimeType(self):
        '''
        The file format media type.
        '''
        raise NotImplementedError

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        raise NotImplementedError

    @classproperty
    def isBinary(self):
        '''
        Tells whether the file format is binary or not.
        '''
        return False

    @classproperty
    def isParseable(self):
        '''
        Tells whether the file format is parseable or not.
        '''
        return False

    @classproperty
    def isExportable(self):
        '''
        Tells whether the file format is exportable or not.
        '''
        return False

    @classproperty
    def isMinifiable(self):
        '''
        Tells whether the file format is minifiable or not.
        '''
        return False

    def __repr__(self):
        '''
        Returns a string representation of this format class.
        '''
        return self.name


class FormatFactory(object):
    '''
    File format factory class.
    '''

    @classmethod
    def fromName(cls, name):
        '''
        Factories a file format class for a given file format name.

        Arguments:
            name (str): The file format name to retrieve a file format class

        Returns:
            Format: The file format class instance

        Raises:
            UnknownFormatError: When a given format is not found
        '''
        format_ = FormatRepository.findByName(name)

        return format_()


class FormatRepository(object):
    '''
    File format repository class.
    '''

    @staticmethod
    def findByName(name, strict=False):
        '''
        Returns the format with the given name.

        Arguments:
            name (str): The file format name
            strict (bool): Whether it should do a loose or strict search

        Returns:
            Format: The file format class

        Raises:
            UnknownFormatError: When a given file format is not found
        '''
        for _format in Format.childs():
            if _format.name == (name if strict else name.lower()):
                return _format

        raise UnknownFormatError('No format found with this name: {}' \
                                     .format(name))

    @staticmethod
    def findByExtension(extension, strict=False):
        '''
        Returns the format with the given extension.

        Arguments:
            extension (str): The file format extension
            strict (bool): Whether it should do a loose or strict search

        Returns:
            Format: The file format class

        Raises:
            UnknownFormatError: When a given file format is not found
        '''
        for _format in Format.childs():
            if (_format.extension
                    == (extension if strict else extension.lower())):
                return _format

        raise UnknownFormatError('No format found with this extension: {}' \
                                     .format(extension))

    @staticmethod
    def findExportableFormats():
        '''
        Returns a list with all exportable formats.

        Returns:
            list: A list with all exportable formats
        '''
        return [format_ for format_ in Format.childs() if format_.isExportable]

    @classmethod
    def listExportableFormatNames(cls):
        '''
        Returns a list with all exportable format names.

        Returns:
            list: A list with all exportable format names
        '''
        return [format_.name for format_ in cls.findExportableFormats()]

    @staticmethod
    def findParseableFormats():
        '''
        Returns a list with all parseable formats.

        Returns:
            list: A list with all parseable formats
        '''
        return [format_ for format_ in Format.childs() if format_.isParseable]

    @classmethod
    def listParseableFormatNames(cls):
        '''
        Returns a list with all parseable format names.

        Returns:
            list: A list with all parseable format names
        '''
        return [format_.name for format_ in cls.findParseableFormats()]

    @staticmethod
    def findMinifiableFormats():
        '''
        Returns a list with all minifiable formats.

        Returns:
            list: A list with all minifiable formats
        '''
        return [format_ for format_ in Format.childs()
                if format_.isExportable and format_.isMinifiable]

    @classmethod
    def listMinifiableFormatNames(cls):
        '''
        Returns a list with all minifiable format names.

        Returns:
            list: A list with all minifiable format names
        '''
        return [format_.name for format_ in cls.findMinifiableFormats()]

    @classmethod
    def groupExportableFormatsByType(cls):
        '''
        Returns a list with all exportable formats grouped by their type.

        Returns:
            list: A list with all exportable formats grouped by their type
        '''
        sorter = lambda format_: format_.type

        return groupby(sorted(cls.findExportableFormats(), key=sorter),
                       key=sorter)


class FormatError(Exception):
    '''
    Generic exception class for file format errors.
    '''
    pass


class UnknownFormatError(FormatError):
    '''
    Exception class raised when a given file format is not found.
    '''
    pass
