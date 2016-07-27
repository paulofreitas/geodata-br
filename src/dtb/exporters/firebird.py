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

import fdb

# Package dependencies

from dtb.exporters import Exporter
from dtb.exporters.sql import SqlExporter
from dtb.formats.firebird import FirebirdFormat

# Classes


class FirebirdExporter(Exporter):
    '''Firebird exporter class.'''

    # Exporter format
    _format = FirebirdFormat

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
