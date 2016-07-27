#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 Paulo Freitas
# MIT License (see LICENSE file)
'''
SQLite 3 file exporter module
'''
from __future__ import absolute_import, unicode_literals

# Imports

# Built-in dependencies

import sqlite3
import tempfile

# Package dependencies

from dtb.exporters import Exporter
from dtb.exporters.sql import SqlExporter
from dtb.formats.sqlite3 import Sqlite3Format

# Classes


class Sqlite3Exporter(Exporter):
    '''SQLite3 exporter class.'''

    # Exporter format
    _format = Sqlite3Format

    @property
    def data(self):
        '''Binary SQLite 3 representation of data.'''
        sql_str = SqlExporter(self._data, self._minified, dialect='sqlite').data

        with tempfile.NamedTemporaryFile() as _sqlite_file:
            with sqlite3.connect(_sqlite_file.name) as sqlite_con:
                sqlite_cursor = sqlite_con.cursor()
                sqlite_cursor.execute('PRAGMA page_size = 1024')
                sqlite_cursor.execute('PRAGMA foreign_keys = ON')
                sqlite_cursor.executescript('BEGIN; {} COMMIT'.format(sql_str))

            with open(_sqlite_file.name, 'rb') as sqlite_file:
                sqlite_data = sqlite_file.read()

        return sqlite_data
