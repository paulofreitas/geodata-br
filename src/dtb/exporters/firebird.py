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
from __future__ import absolute_import

# Imports

# Built-in dependencies

import tempfile

# External dependencies

import fdb

# Package dependencies

from .base import BaseExporter
from .sql import SqlExporter

# Classes


class FirebirdExporter(BaseExporter):
    '''Firebird exporter class.'''

    # Exporter settings
    format = 'Firebird'
    extension = '.fdb'
    binary_format = True

    @property
    def data(self):
        sql_str = SqlExporter(self._data,
                              self._minified,
                              dialect='firebird').data

        _fdb_file = tempfile.mktemp()
        db = fdb.create_database(
            "CREATE DATABASE '{}' USER '{}' PASSWORD '{}'" \
                .format(_fdb_file, 'sysdba', 'masterkey'),
            sql_dialect=3
        )
        cursor = db.cursor()
        in_trans = False

        for stmt in sql_str.rstrip(';').split(';'):
            if stmt.startswith('INSERT') and not in_trans:
                db.begin()
                in_trans = True
            else:
                db.commit()
                in_trans = False

            cursor.execute(stmt)

        with open(_fdb_file, 'rb') as fdb_file:
            fdb_data = fdb_file.read()

        return fdb_data
