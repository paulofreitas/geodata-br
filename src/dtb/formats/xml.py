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

# Package dependencies

from .base import Format

# Classes


class XmlFormat(Format):
    '''The file format class for XML file format.'''

    @property
    def name(self):
        '''The file format name.'''
        return 'xml'

    @property
    def friendlyName(self):
        '''The file format friendly name.'''
        return 'XML'

    @property
    def extension(self):
        '''The file format extension.'''
        return '.xml'

    @property
    def type(self):
        '''The file format type.'''
        return 'Data Interchange'

    @property
    def mimeType(self):
        '''The file format media type.'''
        return ['application/xml', 'text/xml']

    @property
    def info(self):
        '''The file format reference info.'''
        return 'https://en.wikipedia.org/wiki/XML'

    def isExportable(self):
        '''Tells whether the file format is exportable or not.'''
        return True

    def isMinifiable(self):
        '''Tells whether the file format is minifiable or not.'''
        return True
