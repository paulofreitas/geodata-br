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

# Built-in dependencies

from abc import ABCMeta as AbstractClass

# External compatibility dependencies

from future.utils import with_metaclass

# Package metadata

__version__ = '1.0-dev'
__author__ = 'Paulo Freitas <me@paulofreitas.me>'
__copyright__ = 'Copyright (c) 2013-2016 Paulo Freitas'
__license__ = 'MIT License'

# Classes


class Exporter(object, with_metaclass(AbstractClass)):
    '''Abstract base exporter class.'''

    # Exporter format
    _format = None

    def __init__(self, data, minified=False):
        '''Constructor.

        :param data: territorial data to export
        :param minified: whether to minify data when formatting or not
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

        :param _format: the file format name to retrieve an exporter'''
        exporters = {exporter._format().name: exporter
                     for exporter in Exporter.__subclasses__()}

        try:
            return exporters[_format]
        except KeyError:
            raise UnknownExporterError('Unsupported exporting format')


class ExporterError(Exception):
    '''Generic exception class for parsing errors.'''
    pass


class UnknownExporterError(ExporterError):
    '''Exception class raised when a given exporter is not found.'''
    pass
