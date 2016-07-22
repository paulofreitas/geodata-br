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
from __future__ import absolute_import, unicode_literals

# Imports

# Built-in dependencies

import re

from sys import version_info

if version_info >= (3, 0):
    from plistlib import _PlistWriter as PlistWriter, dumps as PlistDumper
else:
    from plistlib import PlistWriter, writePlistToString as PlistDumper

# Package dependencies

from .base import BaseExporter

# Enhancements


def __unsortable_write_dict(self, d):
    self.beginElement('dict')
    items = d.items()

    for key, value in items:
        if not isinstance(key, (str, unicode)):
            raise TypeError('keys must be strings')

        self.simpleElement('key', key)
        self.writeValue(value)

    self.endElement('dict')

PlistWriter.writeDict = __unsortable_write_dict


# Classes


class PlistExporter(BaseExporter):
    '''Property List exporter class.'''

    # Exporter settings
    format = 'Property List'
    extension = '.plist'
    minifiable_format = True

    @property
    def data(self):
        '''Formatted Property List representation of data.'''
        data = self._data.toDict(strKeys=True, forceUnicode=True)
        plist_str = unicode(PlistDumper(data).decode('utf-8'))

        if self._minified:
            plist_str = re.sub('[\n\t]+', '', plist_str)

        return plist_str
