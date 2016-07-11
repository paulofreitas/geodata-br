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

# -- Imports ------------------------------------------------------------------

from __future__ import absolute_import

# Dependency modules

import lxml.etree

# Package modules

from .base import BaseExporter

# -- Implementation -----------------------------------------------------------


class XmlExporter(BaseExporter):
    '''XML exporter class.'''
    format = 'XML'
    extension = '.xml'

    def __str__(self):
        database = lxml.etree.Element('database', name=self._data._name)

        for table_name in self._data._tables:
            if not self._data._dict[table_name]:
                continue

            if not self._minified:
                database.append(
                    lxml.etree.Comment(' Table {} '.format(table_name))
                )

            table = lxml.etree.SubElement(database, 'table', name=table_name)

            for item in self._data._dict[table_name]:
                row = lxml.etree.SubElement(table, 'row')

                for field_name in self._data._fields[table_name]:
                    lxml.etree.SubElement(row, 'field', name=field_name).text =\
                        str(item[field_name]).decode('utf-8')

        return lxml.etree.tostring(database,
                                   pretty_print=not self._minified,
                                   xml_declaration=True,
                                   encoding='utf-8')
