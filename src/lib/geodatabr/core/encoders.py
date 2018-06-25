#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Core encoders module.

This module provides the dataset encoders base functionality.
"""
# Imports

# Built-in dependencies

import abc
import itertools
import sys

# Package dependencies

from geodatabr.core import decorators, i18n, types
from geodatabr.core.utils import io

# Classes


class _EncoderFormat(abc.ABCMeta, decorators.DataDescriptor):
    """Metaclass of encoder format classes."""


class EncoderFormat(types.AbstractClass, metaclass=_EncoderFormat):
    """Base encoder format class."""

    @property
    def name(self) -> str:
        """Gets the encoder format name."""
        raise NotImplementedError

    @property
    def friendlyName(self) -> str:
        """Gets encoder format friendly name."""
        raise NotImplementedError

    @property
    def extension(self) -> str:
        """Gets the encoder format extension."""
        raise NotImplementedError

    @property
    def type(self) -> str:
        """Gets the encoder format type."""
        raise NotImplementedError

    @property
    def mimeType(self):
        """Gets the encoder format media type."""
        raise NotImplementedError

    @property
    def info(self) -> str:
        """Gets the encoder format reference info."""
        raise NotImplementedError

    @property
    def isBinary(self) -> bool:
        """Tells whether the encoder format is binary or not."""
        return False

    def __repr__(self) -> str:
        """
        Returns the canonical string representation of the object.

        Returns:
            The canonical string representation of the object
        """
        attrs = dict(name=self.name, friendlyName=self.friendlyName,
                     extension=self.extension, type=self.type,
                     mimeType=self.mimeType, info=self.info,
                     isBinary=self.isBinary)

        return '{}({})'.format(self.__class__.__name__,
                               ', '.join('{}={}'.format(key, repr(value))
                                         for key, value in attrs.items()))


class EncoderFormatFactory(object):
    """Encoder format factory class."""

    @classmethod
    def fromName(cls, name: str) -> EncoderFormat:
        """
        Factories a encoder format class for a given file format name.

        Args:
            name: The file format name to retrieve a encoder format class

        Returns:
            The encoder format class instance

        Raises:
            geodatabr.core.encoders.UnknownEncoderFormatError:
                If a given encoder format is not found
        """
        format_ = EncoderFormatRepository.findByName(name)

        return format_()


class EncoderFormatRepository(object):
    """Encoder format repository class."""

    @staticmethod
    def findByName(name: str, strict: bool = False) -> EncoderFormat:
        """
        Returns the encoder format with the given name.

        Args:
            name: The encoder format name
            strict: Whether it should do a loose or strict search

        Returns:
            The encoder format class instance

        Raises:
            geodatabr.core.encoders.UnknownEncoderFormatError:
                If a given encoder format is not found
        """
        for encoder_format in EncoderFormat.childs():
            if encoder_format.name == (name if strict else name.lower()):
                return encoder_format()

        raise UnknownEncoderFormatError(
            'No encoder format found with this name: {}'.format(name))

    @staticmethod
    def findByExtension(extension: str, strict: bool = False) -> EncoderFormat:
        """
        Returns the encoder format with the given extension.

        Args:
            extension: The encoder format extension
            strict: Whether it should do a loose or strict search

        Returns:
            The encoder format class instance

        Raises:
            geodatabr.core.encoders.UnknownEncoderFormatError:
                If a given encoder format is not found
        """
        for encoder_format in EncoderFormat.childs():
            if (encoder_format.extension
                    == (extension if strict else extension.lower())):
                return encoder_format()

        raise UnknownEncoderFormatError(
            'No encoder format found with this extension: {}'.format(extension))

    @classmethod
    def listNames(cls) -> types.List:
        """
        Returns a list with all encoder format names.

        Returns:
            A list with all encoder format names
        """
        return types.List(sorted([encoder.format.name
                                  for encoder in Encoder.childs()
                                  if getattr(encoder, 'format')]))

    @classmethod
    def groupByType(cls) -> types.List:
        """
        Returns a list with all encoder formats grouped by their type.

        Returns:
            A list with all encoder formats grouped by their type
        """
        return types.List([(format_type,
                            types.List(sorted(
                                formats,
                                key=lambda _format: _format.friendlyName)))
                           for format_type, formats in itertools.groupby(
                               sorted([encoder.format()
                                       for encoder in Encoder.childs()
                                       if getattr(encoder, 'format')],
                                      key=lambda _format: _format.type),
                               key=lambda _format: _format.type)])


class Encoder(types.AbstractClass):
    """
    Abstract base encoder class.

    Attributes:
        format (geodatabr.core.encoders.EncoderFormat):
            The encoder format class
        serializer (geodatabr.dataset.serializers.BaseSerializer):
            The encoder format serialization class
    """

    format = None
    serializer = None

    def __call__(self, **options) -> io.BinaryFileStream:
        """
        Allows encoding the data into a stream calling the encoder instance.

        Args:
            **options: The encoding options

        Returns:
            A file-like stream

        Raises:
            geodatabr.core.encoders.EncodeError: If data fails to encode
        """
        return self.encode(**options)

    @property
    def options(self) -> dict:
        """Gets the default encoding options."""
        return {}

    @property
    def serializationOptions(self) -> dict:
        """Gets the encoder serialization options."""
        return {}

    def encode(self, data, **options) -> io.BinaryFileStream:
        """
        Encodes the data into a file-like stream.

        Args:
            data: The data to encode
            **options: The encoding options

        Returns:
            A file-like stream

        Raises:
            geodatabr.core.encoders.EncodeError: If data fails to encode
        """
        raise NotImplementedError

    def encodeToFile(self, data, filename: str = None, **options):
        """
        Encodes the data into a file.

        Args:
            data: The data to encode
            filename: The filename to write, if any
            **options: The encoding options

        Raises:
            geodatabr.core.encoders.EncodeError: If data fails to encode
        """
        if not filename:
            filename = i18n._('dataset_name') + self.format.extension

        data = self.encode(data, **options).read()
        output_file = sys.stdout if filename == '-' else open(filename, 'wb')

        if filename == '-':
            data = data.decode()

        with output_file:
            output_file.write(data)


class EncoderFactory(object):
    """Encoder factory class."""

    @classmethod
    def fromFormat(cls, name: str) -> Encoder:
        """
        Factories an encoder class for a given encoder format.

        Args:
            name: The encoder format name to retrieve an encoder

        Returns:
            The encoder class instance

        Raises:
            geodatabr.core.encoders.UnknownEncoderError:
                If a given encoder format is not supported
        """
        for encoder in Encoder.childs():
            if (encoder.format
                    and encoder.serializer
                    and encoder.format.name == name):
                return encoder()

        raise UnknownEncoderError('Unsupported encoder format')


class EncodeError(Exception):
    """Generic exception class for encoding errors."""


class UnknownEncoderFormatError(Exception):
    """Exception class raised when a given encoder format is not found."""


class UnknownEncoderError(Exception):
    """Exception class raised when a given encoder is not found."""
