#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Database exporters package

This package provides the database exporter modules.
'''
from __future__ import absolute_import

# Imports

# Built-in dependencies

import sys

# Package dependencies

from places.core.helpers.filesystem import Path
from places.core.i18n import _, Translator
from places.core.logging import Logger
from places.core.types import AbstractClass

# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2018 Paulo Freitas'
__license__ = 'MIT License'

# Module logging

logger = Logger.instance(__name__)

# Translator setup

Translator.load('databases')

# Classes


class Exporter(AbstractClass):
    '''
    Abstract base exporter class.
    '''

    # Exporter format
    _format = None

    def __init__(self, data):
        '''
        Constructor.

        Arguments:
            data (places.database.entities.DatabaseData): Database data to export
        '''
        self._data = data

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

    def exportToFile(self, filename, **options):
        '''
        Exports the data into a file.

        Arguments:
            filename (str): The filename to write
            options (dict): The exporting options

        Raises:
            ExportError: When data fails to export
        '''
        if options.get('minify'):
            logger.debug('Exporting database to minified %s format...',
                         self.format.friendlyName)
        else:
            logger.debug('Exporting database to %s format...',
                         self.format.friendlyName)

        data = self.export(**options).read()

        logger.debug('Finished exporting database.')

        if not self.format.isBinary and not isinstance(data, unicode):
            data = unicode(data.decode('utf-8'))

        if not filename:
            return sys.stdout.write(data + '\n')

        if filename == 'auto':
            filename = _('database') + self.format.extension

        writeMode = 'wb' if self.format.isBinary else 'w'

        with Path(filename).open(writeMode) as exportFile:
            exportFile.write(data)

    @property
    def format(self):
        '''
        Returns the exporter file format instance.

        Returns:
            places.formats.Format: The exporter file format
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
