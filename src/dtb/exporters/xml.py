#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
XML file exporter module
'''
from __future__ import absolute_import, unicode_literals

# Imports

# External compatibility dependencies

from future.utils import iteritems, itervalues

# External dependencies

from lxml.etree import Comment, Element, SubElement, tostring as xml_str

# Package dependencies

from dtb.exporters import Exporter
from dtb.formats.xml import XmlFormat

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
