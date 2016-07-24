#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Brazilian territorial distribution data exporter

The MIT License (MIT)

Copyright (c) 2013-2016 Paulo Freitas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
from __future__ import absolute_import

# Imports

# Built-in dependencies

from abc import ABCMeta as AbstractClass

# External compatibility dependencies

from future.utils import with_metaclass

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
        exporters = {exporter.format.name: exporter
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
