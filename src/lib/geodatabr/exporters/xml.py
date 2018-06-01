#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
XML file exporter module
'''
# Imports

# Built-in dependencies

import io

# External dependencies

from lxml.etree import Comment, Element, SubElement, tostring as xml_str

# Package dependencies

from geodatabr.exporters import Exporter
from geodatabr.formats.xml import XmlFormat

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
            io.StringIO: A XML file-like stream

        Raises:
            ExportError: When data fails to export
        '''
        data = self._data.normalize(forceStr=True, includeKey=True)
        database = Element('database',
                           name='dtb_{}'.format(self._data._base.year))

        for table_name, rows in iter(data.items()):
            database.append(Comment(' Table {} '.format(table_name)))
            table = SubElement(database, 'table', name=table_name)

            for row_data in iter(rows.values()):
                row = SubElement(table, 'row')

                for column_name, column_value in iter(row_data.items()):
                    SubElement(row, 'field', name=column_name).text =\
                        column_value

        xml_data = xml_str(database,
                           xml_declaration=True,
                           encoding='utf-8',
                           pretty_print=True)

        return io.StringIO(xml_data.decode())
