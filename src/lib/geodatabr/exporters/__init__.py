#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Dataset exporters package

This package provides the dataset exporter modules.
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


class Exporter(AbstractClass):
    '''
    Abstract base exporter class.
    '''

    # Exporter format
    _format = None

    def __call__(self, **options):
        '''
        Allows exporting the data into a stream calling the exporter instance.

        Returns:
            options (dict): The exporting options

        Raises:
            ExportError: When data fails to export
        '''
        return self.export(**options)

    def export(self, **options):
        '''
        Exports the data into a file-like stream.

        Arguments:
            options (dict): The exporting options

        Returns:
            a file-like stream

        Raises:
            ExportError: When data fails to export
        '''
        raise NotImplementedError

    def exportToFile(self, filename='auto', **options):
        '''
        Exports the data into a file.

        Arguments:
            filename (str): The filename to write, if any
            options (dict): The exporting options

        Raises:
            ExportError: When data fails to export
        '''
        formatName = self.format.friendlyName
        extension = self.format.extension

        logger.info('Exporting dataset to %s format...', formatName)

        data = self.export(**options).read()

        logger.debug('Finished exporting database.')

        if not filename:
            return sys.stdout.write(data + '\n')

        if filename == 'auto':
            filename = _('dataset') + extension

        writeMode = 'wb' if self.format.isBinary else 'w'

        with File(filename).open(writeMode) as exportFile:
            exportFile.write(data)

    @property
    def format(self):
        '''
        Returns the exporter file format instance.

        Returns:
            geodatabr.formats.Format: The exporter file format
        '''
        return self._format


class ExporterFactory(object):
    '''
    Exporter factory class.
    '''

    @classmethod
    def fromFormat(cls, _format, *args, **kwargs):
        '''
        Factories an exporter class for a given format.

        Arguments:
            _format (str): The file format name to retrieve an exporter

        Returns:
            Exporter: The exporter class instance

        Raises:
            UnknownExporterError: When a given file format is not found
        '''
        for exporter in Exporter.childs():
            if exporter._format.name == _format:
                return exporter(*args, **kwargs)

        raise UnknownExporterError('Unsupported exporting format')


class ExportError(Exception):
    '''
    Generic exception class for exporting errors.
    '''
    pass


class UnknownExporterError(ExportError):
    '''
    Exception class raised when a given exporter is not found.
    '''
    pass
