#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
XML file exporter module
'''
from __future__ import absolute_import, unicode_literals

# Imports

# Built-in dependencies

import io

# External compatibility dependencies

from future.utils import iteritems, itervalues

# External dependencies

from lxml.etree import Comment, Element, SubElement, tostring as xml_str

# Package dependencies

from places.exporters import Exporter
from places.formats.xml import XmlFormat

# Classes


class XmlExporter(Exporter):
    '''
    XML exporter class.
    '''

    # Exporter format
    _format = XmlFormat

    def export(self, **options):
        '''
        Exports the data into a XML file-like stream.

        Arguments:
            options (dict): The exporting options

        Returns:
            io.BytesIO: A XML file-like stream

        Raises:
            ExportError: When data fails to export
        '''
        data = self._data.normalize(includeKey=True)
        database = Element('database',
                           name='dtb_{}'.format(self._data._base.year))

        for table_name, rows in iteritems(data):
            if not options.get('minify'):
                database.append(Comment(' Table {} '.format(table_name)))

            table = SubElement(database, 'table', name=table_name)

            for row_data in itervalues(rows):
                row = SubElement(table, 'row')

                for column_name, column_value in iteritems(row_data):
                    SubElement(row, 'field', name=column_name).text =\
                        unicode(column_value)

        xml_data = xml_str(database,
                           pretty_print=not options.get('minify'),
                           xml_declaration=True,
                           encoding='utf-8')

        return io.BytesIO(xml_data)
