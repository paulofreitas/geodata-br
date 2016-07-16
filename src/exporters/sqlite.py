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

# -- Imports ------------------------------------------------------------------

# Built-in modules

import sqlite3
import tempfile

# Package modules

from .base import BaseExporter
from .sql import SqlExporter

# -- Implementation -----------------------------------------------------------


class Sqlite3Exporter(BaseExporter):
    '''SQLite3 exporter class.'''
    format = 'SQLite3'
    extension = '.sqlite3'
    binary_format = True

    def __str__(self):
        sql_str = SqlExporter(self._data, self._minified, dialect='sqlite').data

        with tempfile.NamedTemporaryFile() as _sqlite_file:
            with sqlite3.connect(_sqlite_file.name) as sqlite_con:
                sqlite_cursor = sqlite_con.cursor()
                sqlite_cursor.execute('PRAGMA page_size = 1024;')
                sqlite_cursor.executescript('BEGIN; {} COMMIT'.format(sql_str))

            with open(_sqlite_file.name, 'rb') as sqlite_file:
                sqlite_data = sqlite_file.read()

        return sqlite_data
