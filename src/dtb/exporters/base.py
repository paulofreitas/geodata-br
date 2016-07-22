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


class BaseExporter(object, with_metaclass(AbstractClass)):
    '''Base abstract exporter class.'''

    # Whether the exporter format is binary or not
    binary_format = False

    # Whether the exporter format is minifiable or not
    minifiable_format = False

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

    def __str__(self):
        '''String representation of this object.'''
        return self.data
