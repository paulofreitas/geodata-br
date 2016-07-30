#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Database exporters package

This package provides the database exporter modules.
'''
from __future__ import absolute_import

# Imports

# Package dependencies

from dtb.core.types import AbstractClass

# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT License'

# Classes


class Exporter(AbstractClass):
    '''Abstract base exporter class.'''

    # Exporter format
    _format = None

    def __init__(self, data, minified=False):
        '''Constructor.

        Arguments:
            data (dtb.core.entities.TerritorialData): Territorial data to export
            minified (bool): Whether or not it should minify the data
        '''
        self._data = data
        self._minified = minified

    @property
    def data(self):
        '''Formatted data representation.'''
        raise NotImplementedError

    @property
    def format(self):
        '''Returns the exporter file format instance.'''
        if callable(self._format):
            return self._format()

        raise UnknownExporterError('Unsupported exporting format')

    def __str__(self):
        '''String representation of this object.'''
        return self.data


class ExporterFactory(object):
    '''Exporter factory class.'''

    @classmethod
    def fromFormat(cls, _format):
        '''Factories an exporter class for a given format.

        Arguments:
            _format (str): The file format name to retrieve an exporter

        Returns:
            Exporter: The exporter class instance

        Raises:
            UnknownExporterError: When a given file format is not found
        '''
        for exporter in Exporter.childs():
            if exporter._format().name == _format:
                return exporter

        raise UnknownExporterError('Unsupported exporting format')


class ExporterError(Exception):
    '''Generic exception class for parsing errors.'''
    pass


class UnknownExporterError(ExporterError):
    '''Exception class raised when a given exporter is not found.'''
    pass
