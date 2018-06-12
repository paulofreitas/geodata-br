#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
SQL file exporter module
'''
# Imports

# Built-in dependencies

import io

# Package dependencies

from geodatabr.exporters import Exporter
from geodatabr.dataset.schema import Entities
from geodatabr.dataset.serializers import Serializer
from geodatabr.formats.sql import SqlFormat
from geodatabr.formats.sql.utils import SchemaGenerator

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
        data = Serializer(localize=False, includeKey=True).serialize()
        schema = SchemaGenerator(options.get('dialect', 'default'))

        for entity in Entities:
            records = data.get(entity.__table__.name)

            if records:
                schema.addTable(entity.__table__, records)

        return io.StringIO(schema.render())
