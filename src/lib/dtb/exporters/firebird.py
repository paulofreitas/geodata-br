#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
Firebird Embedded file exporter module
'''
from __future__ import absolute_import

# Imports

# Built-in dependencies

import tempfile

# External dependencies

import io
import fdb

# Package dependencies

from dtb.exporters import Exporter
from dtb.exporters.sql import SqlExporter
from dtb.formats.firebird import FirebirdFormat

# Classes


class FirebirdExporter(Exporter):
    '''
    Firebird exporter class.
    '''

    # Exporter format
    _format = FirebirdFormat

    def export(self, **options):
        '''
        Exports the data into a Firebird Embedded file-like stream.

        Arguments:
            options (dict): The exporting options

        Returns:
            io.BytesIO: A Firebird Embedded file-like stream

        Raises:
            ExportError: When data fails to export
        '''
        sql_options = dict(options, dialect='firebird')
        sql_data = SqlExporter(self._data).export(**sql_options)
        fdb_data = io.BytesIO()
        fdb_file = tempfile.mktemp()
        fdb_con = fdb.create_database(
            "CREATE DATABASE '{}' USER '{}' PASSWORD '{}'" \
                .format(fdb_file, 'sysdba', 'masterkey'),
            sql_dialect=3
        )
        fdb_cursor = fdb_con.cursor()
        in_trans = False

        for stmt in sql_data.read().rstrip(';').split(';'):
            if stmt.startswith('INSERT') and not in_trans:
                fdb_con.begin()
                in_trans = True
            else:
                fdb_con.commit()
                in_trans = False

            fdb_cursor.execute(stmt)

        fdb_data.write(fdb_file.read())
        fdb_data.seek(0)

        return fdb_data
