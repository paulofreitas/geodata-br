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


class Format(object, with_metaclass(AbstractClass)):
    '''Abstract file format base class.'''

    @property
    def name(self):
        '''The file format name.'''
        raise NotImplementedError

    @property
    def friendlyName(self):
        '''The file format friendly name.'''
        raise NotImplementedError

    @property
    def extension(self):
        '''The file format extension.'''
        raise NotImplementedError

    @property
    def type(self):
        '''The file format type.'''
        raise NotImplementedError

    @property
    def mimeType(self):
        '''The file format media type.'''
        raise NotImplementedError

    @property
    def info(self):
        '''The file format reference info.'''
        raise NotImplementedError

    def isBinary(self):
        '''Tells whether the file format is binary or not.'''
        return False

    def isParseable(self):
        '''Tells whether the file format is parseable or not.'''
        return False

    def isExportable(self):
        '''Tells whether the file format is exportable or not.'''
        return False

    def isMinifiable(self):
        '''Tells whether the file format is minifiable or not.'''
        return False


class FormatFactory(object):
    '''File format factory class.'''

    @classmethod
    def fromName(cls, name):
        '''Factories a file format class for a given file format name.

        :param name: the file format name to retrieve a file format instance'''
        formats = {format.name: _format for _format in Format.__subclasses__()}

        try:
            return formats[name]
        except KeyError:
            raise UnknownFormatError('No format found with this name: {}' \
                                         .format(name))


class FormatError(Exception):
    '''Generic exception class for file format errors.'''
    pass


class UnknownFormatError(FormatError):
    '''Exception class raised when a given file format is not found.'''
    pass
