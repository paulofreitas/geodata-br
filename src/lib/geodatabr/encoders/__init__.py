#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Dataset encoders package.

This package provides the dataset encoder modules.
'''
# Imports

# Built-in dependencies

import sys

from itertools import groupby

# Package dependencies

from geodatabr import __version__, __author__, __copyright__, __license__
from geodatabr.core.helpers.filesystem import File
from geodatabr.core.i18n import _, Translator
from geodatabr.core.types import AbstractClass

# Translator setup

Translator.load('dataset')

# Classes


class EncoderFormat(AbstractClass):
    '''Abstract encoder file format base class.'''

    @property
    def name(self) -> str:
        '''Gets the encoder format name.'''
        raise NotImplementedError

    @property
    def friendlyName(self) -> str:
        '''Gets encoder format friendly name.'''
        raise NotImplementedError

    @property
    def extension(self) -> str:
        '''Gets the encoder format extension.'''
        raise NotImplementedError

    @property
    def type(self) -> str:
        '''Gets the encoder format type.'''
        raise NotImplementedError

    @property
    def mimeType(self):
        '''Gets the encoder format media type.'''
        raise NotImplementedError

    @property
    def info(self) -> str:
        '''Gets the encoder format reference info.'''
        raise NotImplementedError

    @property
    def isBinary(self) -> bool:
        '''Tells whether the encoder format is binary or not.'''
        return False

    def __repr__(self) -> str:
        '''Returns a string representation of this encoder format class.'''
        return self.name


class EncoderFormatFactory(object):
    '''Encoder format factory class.'''

    @classmethod
    def fromName(cls, name: str) -> EncoderFormat:
        '''
        Factories a encoder format class for a given file format name.

        Args:
            name: The file format name to retrieve a encoder format class

        Returns:
            The encoder format class instance

        Raises:
            geodatabr.encoders.UnknownEncoderFormatError:
                If a given encoder format is not found
        '''
        format_ = EncoderFormatRepository.findByName(name)

        return format_()


class EncoderFormatRepository(object):
    '''Encoder format repository class.'''

    @staticmethod
    def findByName(name: str, strict: bool = False) -> EncoderFormat:
        '''
        Returns the encoder format with the given name.

        Args:
            name: The encoder format name
            strict: Whether it should do a loose or strict search

        Returns:
            The encoder format class

        Raises:
            geodatabr.encoders.UnknownEncoderFormatError:
                If a given encoder format is not found
        '''
        for _format in EncoderFormat.childs():
            if _format.name == (name if strict else name.lower()):
                return _format

        raise UnknownEncoderFormatError(
            'No encoder format found with this name: {}'.format(name))

    @staticmethod
    def findByExtension(extension: str, strict: bool = False) -> EncoderFormat:
        '''
        Returns the encoder format with the given extension.

        Args:
            extension: The encoder format extension
            strict: Whether it should do a loose or strict search

        Returns:
            The encoder format class

        Raises:
            geodatabr.encoders.UnknownEncoderFormatError:
                If a given encoder format is not found
        '''
        for _format in EncoderFormat.childs():
            if (_format.extension
                    == (extension if strict else extension.lower())):
                return _format

        raise UnknownEncoderFormatError(
            'No encoder format found with this extension: {}'.format(extension))

    @classmethod
    def listNames(cls) -> list:
        '''
        Returns a list with all encoder format names.

        Returns:
            A list with all encoder format names
        '''
        return list(sorted([encoder.format().name
                            for encoder in Encoder.childs()
                            if getattr(encoder, 'format')]))

    @classmethod
    def groupByType(cls) -> list:
        '''
        Returns a list with all encoder formats grouped by their type.

        Returns:
            A list with all encoder formats grouped by their type
        '''
        sorter = lambda format_: format_.type

        return list(groupby(
            sorted([encoder.format()
                    for encoder in Encoder.childs()
                    if getattr(encoder, 'format')],
                   key=sorter),
            key=sorter))


class Encoder(AbstractClass):
    '''
    Abstract base encoder class.

    Attributes:
        format (geodatabr.encoders.EncoderFormat): The encoder format class
        serializer: The encoder format serialization class
    '''

    format = None
    serializer = None

    def __call__(self, **options):
        '''
        Allows encoding the data into a stream calling the encoder instance.

        Returns:
            **options: The encoding options

        Raises:
            geodatabr.encoders.EncodeError: If data fails to encode
        '''
        return self.encode(**options)

    @property
    def options(self) -> dict:
        '''Gets the default encoding options.'''
        return {}

    @property
    def serializationOptions(self) -> dict:
        '''Gets the encoder serialization options.'''
        return {}

    def encode(self, data, **options):
        '''
        Encodes the data into a file-like stream.

        Args:
            data: The data to encode
            **options: The encoding options

        Returns:
            io.IOBase: a file-like stream

        Raises:
            geodatabr.encoders.EncodeError: If data fails to encode
        '''
        raise NotImplementedError

    def encodeToFile(self, data, filename: str = 'auto', **options):
        '''
        Encodes the data into a file.

        Args:
            data: The data to encode
            filename: The filename to write, if any
            **options: The encoding options

        Raises:
            geodatabr.encoders.EncodeError: If data fails to encode
        '''
        data = self.encode(data, **options).read()

        if not filename:
            return sys.stdout.write(data + '\n')

        if filename == 'auto':
            filename = _('dataset_name') + self.format.extension

        with File(filename) \
            .open('wb' if self.format.isBinary else 'w') as _file:
            _file.write(data)


class EncoderFactory(object):
    '''Encoder factory class.'''

    @classmethod
    def fromFormat(cls, name: str) -> Encoder:
        '''
        Factories an encoder class for a given encoder format.

        Args:
            name: The encoder format name to retrieve an encoder

        Returns:
            The encoder class instance

        Raises:
            geodatabr.encoders.UnknownEncoderError:
                If a given encoder format is not supported
        '''
        for encoder in Encoder.childs():
            if (encoder.format
                    and encoder.serializer
                    and encoder.format().name == name):
                return encoder()

        raise UnknownEncoderError('Unsupported encoder format')


class EncodeError(Exception):
    '''Generic exception class for encoding errors.'''
    pass


class UnknownEncoderFormatError(Exception):
    '''Exception class raised when a given encoder format is not found.'''
    pass


class UnknownEncoderError(Exception):
    '''Exception class raised when a given encoder is not found.'''
    pass
