#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
SQLite 3 file exporter module
'''
# Imports

# Built-in dependencies

import io
import sqlite3
import tempfile

# Package dependencies

from geodatabr.exporters import Exporter
from geodatabr.exporters.sql import SqlExporter
from geodatabr.formats.sqlite3 import Sqlite3Format

# Classes


class Sqlite3Exporter(Exporter):
    '''
    SQLite3 exporter class.
    '''

    # Exporter format
    _format = Sqlite3Format

    def export(self, **options):
        '''
        Exports the data into a SQLite 3 file-like stream.

        Arguments:
            options (dict): The exporting options

        Returns:
            io.BytesIO: A SQLite 3 file-like stream

        Raises:
            ExportError: When data fails to export
        '''
        sql_options = dict(options, dialect='sqlite')
        sql_data = SqlExporter().export(**sql_options)
        sqlite_data = io.BytesIO()

        with tempfile.NamedTemporaryFile() as sqlite_file:
            with sqlite3.connect(sqlite_file.name) as sqlite_con:
                sqlite_cursor = sqlite_con.cursor()
                sqlite_cursor.execute('PRAGMA page_size = 1024')
                sqlite_cursor.execute('PRAGMA foreign_keys = ON')
                sqlite_cursor.executescript('BEGIN; {} COMMIT' \
                                                .format(sql_data.read()))

            sqlite_data.write(sqlite_file.read())
            sqlite_data.seek(0)

        return sqlite_data
