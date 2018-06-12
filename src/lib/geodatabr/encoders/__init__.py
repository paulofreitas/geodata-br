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

# Package dependencies

from geodatabr import __version__, __author__, __copyright__, __license__
from geodatabr.core.helpers.filesystem import File
from geodatabr.core.i18n import _, Translator
from geodatabr.core.logging import Logger
from geodatabr.core.types import AbstractClass

# Module logging

logger = Logger.instance(__name__)

# Translator setup

Translator.load('dataset')

# Classes


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


class EncodeError(Exception):
    '''
    Generic exception class for encoding errors.
    '''
    pass


class UnknownEncoderError(EncodeError):
    '''
    Exception class raised when a given encoder is not found.
    '''
    pass
