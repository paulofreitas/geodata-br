#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Firebird Embedded file encoder module
'''
# Imports

# Built-in dependencies

import tempfile

# External dependencies

import io
import fdb

# Package dependencies

from geodatabr.core.helpers.filesystem import File
from geodatabr.encoders import Encoder
from geodatabr.encoders.sql import SqlEncoder
from geodatabr.formats.firebird import FirebirdFormat

# Classes


class FirebirdEncoder(Encoder):
    '''
    Firebird encoder class.
    '''

    # Encoder format
    _format = FirebirdFormat

    def encode(self, **options):
        '''
        Encodes the data into a Firebird Embedded file-like stream.

        Arguments:
            options (dict): The encoding options

        Returns:
            io.BytesIO: A Firebird Embedded file-like stream

        Raises:
            geodatabr.encoders.EncodeError: When data fails to encode
        '''
        sql_options = dict(options, dialect='firebird')
        sql_data = SqlEncoder().encode(**sql_options)
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

        fdb_data.write(File(fdb_file).readBytes())
        fdb_data.seek(0)

        return fdb_data
