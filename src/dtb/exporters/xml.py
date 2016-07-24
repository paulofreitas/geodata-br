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

# External compatibility dependencies

from future.utils import iteritems, itervalues

# External dependencies

from lxml.etree import Comment, Element, SubElement, tostring as xml_str

# Package dependencies

from ..formats.xml import XmlFormat
from .base import Exporter

# Classes


class XmlExporter(Exporter):
    '''XML exporter class.'''

    # Exporter format
    _format = XmlFormat

    @property
    def data(self):
        '''Formatted XML representation of data.'''
        data = self._data.toDict(includeKey=True)
        database = Element('database', name=self._data._name)

        for table_name, rows in iteritems(data):
            if not self._minified:
                database.append(Comment(' Table {} '.format(table_name)))

            table = SubElement(database, 'table', name=table_name)

            for row_data in itervalues(rows):
                row = SubElement(table, 'row')

                for column_name, column_value in iteritems(row_data):
                    SubElement(row, 'field', name=column_name).text =\
                        unicode(column_value)

        return xml_str(database,
                       pretty_print=not self._minified,
                       xml_declaration=True,
                       encoding='utf-8')
