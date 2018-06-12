#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
SQLite 3 file encoder module
'''
# Imports

# Built-in dependencies

import io
import sqlite3
import tempfile

# Package dependencies

from geodatabr.core.helpers.decorators import classproperty
from geodatabr.encoders import Encoder, Format
from geodatabr.encoders.sql import SqlEncoder

# Classes


class Sqlite3Format(Format):
    '''
    The file format class for SQLite 3 file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'sqlite3'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'SQLite 3'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.sqlite3'

    @classproperty
    def type(self):
        '''
        The file format type.
        '''
        return 'Database'

    @classproperty
    def mimeType(self):
        '''
        The file format media type.
        '''
        return 'application/x-sqlite3'

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        return 'https://en.wikipedia.org/wiki/SQLite'

    @classproperty
    def isBinary(self):
        '''
        Tells whether the file format is binary or not.
        '''
        return True

    @classproperty
    def isExportable(self):
        '''
        Tells whether the file format is exportable or not.
        '''
        return True


class Sqlite3Encoder(Encoder):
    '''
    SQLite3 encoder class.
    '''

    # Encoder format
    _format = Sqlite3Format

    def encode(self, **options):
        '''
        Encodes the data into a SQLite 3 file-like stream.

        Arguments:
            options (dict): The encoding options

        Returns:
            io.BytesIO: A SQLite 3 file-like stream

        Raises:
            geodatabr.encoders.EncodeError: When data fails to encode
        '''
        sql_options = dict(options, dialect='sqlite')
        sql_data = SqlEncoder().encode(**sql_options)
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
