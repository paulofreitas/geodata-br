#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Dataset encoders package

This package provides the dataset encoder modules.
'''
# Imports

# Built-in dependencies

import sys

from itertools import groupby

# Package dependencies

from geodatabr import __version__, __author__, __copyright__, __license__
from geodatabr.core.helpers.decorators import classproperty
from geodatabr.core.helpers.filesystem import File
from geodatabr.core.i18n import _, Translator
from geodatabr.core.logging import Logger
from geodatabr.core.types import AbstractClass

# Module logging

logger = Logger.instance(__name__)

# Translator setup

Translator.load('dataset')

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
    def isExportable(self):
        '''
        Tells whether the file format is exportable or not.
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


class Encoder(AbstractClass):
    '''
    Abstract base encoder class.
    '''

    # Encoder format
    _format = None

    def __call__(self, **options):
        '''
        Allows encoding the data into a stream calling the encoder instance.

        Returns:
            options (dict): The encoding options

        Raises:
            geodatabr.encoders.EncodeError: When data fails to encode
        '''
        return self.encode(**options)

    def encode(self, **options):
        '''
        Encodes the data into a file-like stream.

        Arguments:
            options (dict): The encoding options

        Returns:
            io.IOBase: a file-like stream

        Raises:
            geodatabr.encoders.EncodeError: When data fails to encode
        '''
        raise NotImplementedError

    def encodeToFile(self, filename='auto', **options):
        '''
        Encodes the data into a file.

        Arguments:
            filename (str): The filename to write, if any
            options (dict): The encoding options

        Raises:
            geodatabr.encoders.EncodeError: When data fails to encode
        '''
        formatName = self.format.friendlyName
        extension = self.format.extension

        logger.info('Encoding dataset to %s format...', formatName)

        data = self.encode(**options).read()

        logger.debug('Finished encoding dataset.')

        if not filename:
            return sys.stdout.write(data + '\n')

        if filename == 'auto':
            filename = _('dataset_name') + extension

        writeMode = 'wb' if self.format.isBinary else 'w'

        with File(filename).open(writeMode) as _file:
            _file.write(data)

    @property
    def format(self):
        '''
        Returns the encoder file format instance.

        Returns:
            geodatabr.formats.Format: The encoder file format
        '''
        return self._format


class EncoderFactory(object):
    '''
    Encoder factory class.
    '''

    @classmethod
    def fromFormat(cls, _format, *args, **kwargs):
        '''
        Factories an encoder class for a given format.

        Arguments:
            _format (str): The file format name to retrieve an encoder

        Returns:
            geodatabr.encoders.Encoder: The encoder class instance

        Raises:
            geodatabr.encoders.UnknownEncoderError:
                When a given file format is not supported
        '''
        for encoder in Encoder.childs():
            if encoder._format.name == _format:
                return encoder(*args, **kwargs)

        raise UnknownEncoderError('Unsupported encoding format')


class FormatError(Exception):
    '''
    Generic exception class for file format errors.
    '''
    pass


class EncodeError(Exception):
    '''
    Generic exception class for encoding errors.
    '''
    pass


class UnknownFormatError(FormatError):
    '''
    Exception class raised when a given file format is not found.
    '''
    pass


class UnknownEncoderError(EncodeError):
    '''
    Exception class raised when a given encoder is not found.
    '''
    pass
