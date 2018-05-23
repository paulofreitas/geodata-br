#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
SQL file exporter module
'''
from __future__ import absolute_import

# Imports

# Built-in dependencies

import io

# Package dependencies

from places.exporters import Exporter
from places.formats.sql import SqlFormat
from places.formats.sql.utils import SchemaGenerator

# Classes


class SqlExporter(Exporter):
    '''
    SQL exporter class.
    '''

    # Exporter format
    _format = SqlFormat

    def export(self, **options):
        '''
        Exports the data into a SQL file-like stream.

        Arguments:
            options (dict): The exporting options

        Returns:
            io.StringIO: A SQL file-like stream

        Raises:
            ExportError: When data fails to export
        '''
        schema = SchemaGenerator(options.get('dialect', 'default'),
                                 options.get('minify'))

        for entity in self._data._base.entities:
            data = self._data.records[entity.__table__.name]

            if data:
                table = schema.createTable(entity)
                table._data = data

        return io.StringIO(schema.render())
