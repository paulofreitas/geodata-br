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

from geodatabr.core.helpers.decorators import classproperty
from geodatabr.core.helpers.filesystem import File
from geodatabr.encoders import Encoder, Format
from geodatabr.encoders.sql import SqlEncoder

# Classes


class FirebirdFormat(Format):
    '''
    The file format class for Firebird Embedded file format.
    '''

    @classproperty
    def name(self):
        '''
        The file format name.
        '''
        return 'firebird'

    @classproperty
    def friendlyName(self):
        '''
        The file format friendly name.
        '''
        return 'Firebird Embedded'

    @classproperty
    def extension(self):
        '''
        The file format extension.
        '''
        return '.fdb'

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
        return None

    @classproperty
    def info(self):
        '''
        The file format reference info.
        '''
        return 'https://en.wikipedia.org/wiki/Embedded_database#Firebird_Embedded'

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
